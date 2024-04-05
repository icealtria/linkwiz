use std::env;
use std::process;
use linkwiz;


fn main() {
    if !cfg!(target_os = "linux") {
        println!("LinkWiz is only supported on Linux.");
    }

    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        println!("Usage: linkwiz [install | uninstall | <url>]");
        process::exit(1);
    }

    let arg = &args[1];

    match arg.as_str() {
        "install" => linkwiz::install(env::current_exe().unwrap().to_str().unwrap()),
        "uninstall" => linkwiz::uninstall(),
        _ => linkwiz::core::process_url(arg),
    }
}
