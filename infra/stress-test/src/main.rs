use std::collections::HashMap;

use reqwest::header::{HeaderMap, CONTENT_TYPE};
use reqwest::{Client, Result};

async fn put_employee(client: &Client, instance: char, index: u8) -> Result<()> {
    let body = HashMap::from([
        ("name", format!("name-{}", index)),
        ("email", format!("email-{}@domain.tld", index)),
        ("address_line1", format!("line 1 -{}", index)),
        ("address_line2", format!("line 2 -{}", index)),
        ("city", "Paris".to_string()),
        ("zip_code", format!("75-{}", index)),
    ]);
    println!("instance {}: putting employee {}", instance, index);
    let url = format!("https://{}.hr.dmerej.info/api/v1/employee", instance);
    let response = client.put(url).json(&body).send().await?;
    response.error_for_status()?;
    Ok(())
}

#[tokio::main]
async fn main() -> Result<()> {
    let mut default_headers = HeaderMap::new();
    default_headers.insert(CONTENT_TYPE, "application/json".parse().unwrap());
    let client = Client::builder()
        .connection_verbose(true)
        .default_headers(default_headers)
        .build()?;
    for instance in 'a'..'c' {
        for index in 1..3 {
            put_employee(&client, instance, index).await?;
        }
    }
    Ok(())
}
