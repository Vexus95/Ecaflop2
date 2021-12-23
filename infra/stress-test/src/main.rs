use std::collections::HashMap;

use anyhow::{Context, Result};
use futures::StreamExt;
use reqwest::header::{HeaderMap, CONTENT_TYPE};
use reqwest::Client;

async fn put_employee(client: &Client, instance: char, index: u8) -> Result<()> {
    let body = HashMap::from([
        ("name", format!("name-{}", index)),
        ("email", format!("email-{}@domain.tld", index)),
        ("address_line1", format!("line 1 -{}", index)),
        ("address_line2", format!("line 2 -{}", index)),
        ("city", "Paris".to_string()),
        ("zip_code", format!("75-{}", index)),
    ]);
    if index % 10 == 0 {
        println!("instance {} employe {}", instance, index);
    }
    let url = format!("https://{}.hr.dmerej.info/api/v1/employee", instance);
    let response = client
        .put(url)
        .json(&body)
        .send()
        .await
        .with_context(|| format!("instance : {} could not put employee {}", instance, index))?;

    response
        .error_for_status()
        .with_context(|| format!("instance : {} could not put employee {}", instance, index))?;

    Ok(())
}

async fn put_employees(client: &Client, instance: char) -> Result<()> {
    for index in 1..=100 {
        put_employee(&client, instance, index).await?;
    }
    Ok(())
}

fn main() -> Result<()> {
    let rt = tokio::runtime::Builder::new_multi_thread()
        .worker_threads(4)
        .enable_all()
        .build()
        .unwrap();

    rt.block_on(perf_test())
}

async fn perf_test() -> Result<()> {
    let mut default_headers = HeaderMap::new();
    default_headers.insert(CONTENT_TYPE, "application/json".parse().unwrap());
    let client = Client::builder()
        .connection_verbose(true)
        .default_headers(default_headers)
        .build()?;

    let instances: Vec<_> = ('a'..='z').collect();
    let stream = futures::stream::iter(instances.into_iter().map(|c| {
        let client = client.clone();
        tokio::spawn(async move { stress_instance(&client, c).await })
    }))
    .buffer_unordered(3)
    .map(|r| {
        let result = r.unwrap(); // unwrap JoinHerror
        if let Err(e) = result {
            eprint!("{:?}", e.source());
        }
    })
    .collect::<Vec<_>>();
    stream.await;

    Ok(())
}

async fn stress_instance(client: &Client, instance: char) -> Result<()> {
    put_employees(&client, instance).await
}
