use url::Url;

use crate::{browsers::Browser, config::RulesConfig};

pub fn match_url(browsers: Vec<Browser>, url: &Url, config: RulesConfig) -> Option<Browser> {
    None
}
