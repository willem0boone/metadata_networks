# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
# CRAN packages
cran_pkgs <- c(
  "dplyr",
  "lubridate",
  "leaflet",
  "htmlwidgets",
  "htmltools",
  "usethis",
  "purrr", 
  "stringr",
  "yaml"
  
)


install_if_missing(cran_pkgs)

# GitHub package
install_github_if_missing("inbo/etn", "etn")

# ------------------------------------------------------------------------------
# load packages
invisible(lapply(cran_pkgs, library, character.only = TRUE))
library(etn)

# ------------------------------------------------------------------------------

config <- yaml::read_yaml("ETN_ARMS_search_config.yaml")


deployments <- get_acoustic_deployments() %>%
  select(all_of(config$cols))

for (col in names(config$filters)) {
  values <- config$filters[[col]]
  
  if (col == "station_name") {
    deployments <- deployments %>%
      filter(str_detect(.data[[col]], 
                        regex(paste(values, collapse = "|"), ignore_case = TRUE)))
  } else {
    deployments <- deployments %>%
      filter(.data[[col]] %in% values)
  }
}

deployments <- deployments %>%
  distinct(deploy_date_time, .keep_all = TRUE)


write.csv(deployments, "output/deployments_ARMS.csv")

