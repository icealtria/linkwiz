use url::Url;

pub fn process_url(url: &str) {
    let parsed_url = Url::parse(url).expect("Failed to parse url");

    match parsed_url.scheme() {
        "http" | "https" => {}
        _ => {
            println!("Unsupported scheme: {}", parsed_url.scheme());
            std::process::exit(1);
        }
    }
}
