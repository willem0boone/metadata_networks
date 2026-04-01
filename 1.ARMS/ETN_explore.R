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
# get col names
col_names = names(get_acoustic_deployments())

write.csv(col_names, "lookup/acoustic_deployments_col_names.csv")


# ------------------------------------------------------------------------------
# find uniqe project code

deployments <- get_acoustic_deployments()

df_acoustic_project_code <- deployments %>%
  distinct(acoustic_project_code) %>%
  arrange(acoustic_project_code)

write.csv(df_acoustic_project_code, "lookup/acoustic_deployments_project_codes.csv")

df_station_name <- deployments %>%
  distinct(station_name) %>%
  arrange(station_name)

write.csv(df_acoustic_project_code, "lookup/acoustic_deployments_station_names.csv")

# ------------------------------------------------------------------------------