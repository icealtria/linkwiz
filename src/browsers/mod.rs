use std::path::PathBuf;
pub struct Browser {
    pub name: String,
    pub exec: PathBuf,
}

#[cfg(target_os = "linux")]
mod linux;

#[cfg(target_os = "windows")]
mod windows;

#[cfg(target_os = "linux")]
pub use linux::get_browsers;

#[cfg(target_os = "windows")]
pub use windows::get_browsers;
