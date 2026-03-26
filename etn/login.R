# ------------------------------------
# helper: install CRAN packages if missing
install_if_missing <- function(pkgs) {
  missing <- pkgs[!pkgs %in% rownames(installed.packages())]
  if (length(missing) > 0) {
    install.packages(missing)
  }
}

# helper: install GitHub packages if missing
install_github_if_missing <- function(repo, pkg_name) {
  if (!pkg_name %in% rownames(installed.packages())) {
    if (!"pak" %in% rownames(installed.packages())) {
      install.packages("pak")
    }
    pak::pak(repo)
  }
}

# ------------------------------------
# CRAN packages
cran_pkgs <- c(
  "dplyr",
  "lubridate",
  "leaflet",
  "htmlwidgets",
  "htmltools",
  "usethis"
)

install_if_missing(cran_pkgs)

# GitHub package
install_github_if_missing("inbo/etn", "etn")

# ------------------------------------
# load packages
invisible(lapply(cran_pkgs, library, character.only = TRUE))
library(etn)

# ------------------------------------
# run only in interactive sessions
if (interactive()) {
  usethis::edit_r_environ()
}

# ------------------------------------
# your code
deployments <- get_acoustic_deployments()
deployments