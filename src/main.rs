use linkwiz_rs;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() != 3 || args[1] != "url" {
        eprintln!("Usage: linkwiz url <url>");
        return;
    }

    let url = &args[2];
    println!("Processing URL: {}", url);
    linkwiz_rs::core::process_url(url);
}
