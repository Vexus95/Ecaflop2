use anyhow::{bail, ensure, Result};
use clap::Parser;
use reqwest::header::{HeaderMap, CONTENT_TYPE};
use reqwest::Client;
use std::collections::HashMap;
use std::fmt::Display;

#[derive(Clone)]
pub struct Config {
    pub base_url: String,
    pub verbose: bool,
    pub dry_run: bool,
}

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    #[arg(long)]
    base_url: String,
    #[arg(long, default_value_t = 1)]
    instances: usize,
    #[arg(long, default_value_t = false)]
    dry_run: bool,
    #[arg(long, default_value_t = false)]
    verbose: bool,
    #[arg(long, default_value_t = 1)]
    threads: usize,
    #[arg(long, default_value_t = 1)]
    employees: usize,
}

#[derive(Debug)]
struct StressTest {
    url: String,
    employees: usize,
}

impl Display for StressTest {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "Stress test for {} with {} employees",
            self.url, self.employees
        )
    }
}

impl StressTest {
    async fn run(&self, config: &Config) -> Result<()> {
        let mut default_headers = HeaderMap::new();
        default_headers.insert(CONTENT_TYPE, "application/json".parse().unwrap());
        let client = Client::builder().default_headers(default_headers).build()?;
        let mut num_errors = 0;
        for index in 1..=self.employees {
            if let Err(e) = self.insert_employee(&client, config, index).await {
                eprintln!("{e:#}");
                num_errors += 1;
            }
        }
        ensure!(num_errors == 0, "{self} failed with {num_errors} error(s)");
        Ok(())
    }

    async fn insert_employee(&self, client: &Client, config: &Config, index: usize) -> Result<()> {
        if config.verbose {
            println!("{}: inserting employee {}", self.url, index);
        }
        if config.dry_run {
            return Ok(());
        }
        let body = HashMap::from([
            ("name", format!("name-{}", index)),
            ("email", format!("email-{}@domain.tld", index)),
            ("address_line1", format!("line 1 -{}", index)),
            ("address_line2", format!("line 2 -{}", index)),
            ("city", "Paris".to_string()),
            ("zip_code", format!("75{}", index)),
            ("hiring_date", "2025-01-01".to_owned()),
            ("job_title", "dev".to_owned()),
        ]);
        let full_url = format!("{}/add_employee", self.url);
        let response = client.post(full_url).form(&body).send().await?;

        let status = response.status();
        let text = response.text().await?;

        if status.is_client_error() || status.is_server_error() {
            bail!("request failed with satus {status}\nBody:\n{text}\n");
        }
        Ok(())
    }
}

async fn run_tests(tests: Vec<StressTest>, config: &Config) -> Vec<Result<()>> {
    let mut tasks = vec![];
    for test in tests {
        let config = config.clone();
        let task = tokio::spawn(async move { test.run(&config).await });
        tasks.push(task);
    }
    let mut outputs = vec![];
    for task in tasks {
        outputs.push(task.await.unwrap());
    }
    outputs
}

pub fn run() -> Result<()> {
    let args = Args::parse();

    let Args {
        base_url,
        instances,
        dry_run,
        verbose,
        threads,
        employees,
    } = args;

    let urls = get_urls(&base_url, instances)?;
    let tests: Vec<StressTest> = urls
        .into_iter()
        .map(|url| StressTest { url, employees })
        .collect();

    let config = Config {
        base_url,
        dry_run,
        verbose,
    };

    let rt = tokio::runtime::Builder::new_multi_thread()
        .worker_threads(threads)
        .enable_all()
        .build()
        .unwrap();

    let outcomes = rt.block_on(run_tests(tests, &config));
    for outcome in outcomes {
        if let Err(e) = outcome {
            println!("{e}");
        }
    }
    Ok(())
}

fn get_urls(base_url: &str, count: usize) -> Result<Vec<String>> {
    if base_url.contains("localhost") || base_url.contains("127.0.0.") {
        if count != 1 {
            bail!("Can only stress one instance when using localhost");
        }
        return Ok(vec![base_url.to_string()]);
    }

    let parts: Vec<_> = base_url.split("://").collect();
    if parts.len() != 2 {
        bail!("Expected <protocol>://<domain> url");
    }
    let protocol = &parts[0];
    let rest = &parts[1];

    let mut res = vec![];
    let mut ascii_value = b'a';
    for _ in 0..count {
        let letter = ascii_value as char;
        res.push(format!("{protocol}://{letter}.{rest}"));
        ascii_value += 1;
    }
    Ok(res)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generate_instances_names_when_localhost() {
        let actual = get_urls("http://localhost:8000", 1).unwrap();
        assert_eq!(actual, &["http://localhost:8000"]);
    }

    #[test]
    fn test_generate_instances_names_when_127_0_0_1() {
        let actual = get_urls("http://127.0.0.1:8000", 1).unwrap();
        assert_eq!(actual, &["http://127.0.0.1:8000"]);
    }

    #[test]
    fn test_generate_instances_by_letters() {
        let actual = get_urls("https://domain.tld", 3).unwrap();
        assert_eq!(
            actual,
            &[
                "https://a.domain.tld",
                "https://b.domain.tld",
                "https://c.domain.tld",
            ]
        );
    }
}
