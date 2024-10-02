use url::Url;

pub fn hostname_port_from_url (url: &Url) -> String {
    let url_host = url.host_str().unwrap_or("");
    let url_port = match url.port() {
        Some(port) => format!(":{}", port),
        None => "".to_string(),
    };
    format!("{}{}", url_host, url_port)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_host_port_from_url() {
        let urls = vec![
            Url::parse("http://example.com").unwrap(),
            Url::parse("https://example.com").unwrap(),
            Url::parse("https://example.com:8443/path?query=value#fragment").unwrap(),
            Url::parse("http://127.0.0.1:8080/").unwrap(),
            Url::parse("http://localhost:8080/path").unwrap(),
        ];

        let expected = vec![
            "example.com",
            "example.com",
            "example.com:8443",
            "127.0.0.1:8080",
            "localhost:8080",
        ];

        let output: Vec<String> = urls.iter().map(|url| hostname_port_from_url(url)).collect();
        assert_eq!(output, expected);
    }
}
