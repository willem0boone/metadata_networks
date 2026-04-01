# ------------------------------------------------------------------------------
run_etn_pipeline <- function(output_csv_path) {
  
  # ----------------------------------------------------------------------------
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
  
  # ----------------------------------------------------------------------------
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
  
  # ----------------------------------------------------------------------------
  # load packages
  invisible(lapply(cran_pkgs, library, character.only = TRUE))
  library(etn)
  
  # ----------------------------------------------------------------------------
  # read config
  config <- yaml::read_yaml("config/config_ETN_ARMS_search.yaml")
  
  # ----------------------------------------------------------------------------
  # main logic
  deployments <- get_acoustic_deployments() %>%
    dplyr::select(dplyr::all_of(config$cols))
  
  for (col in names(config$filters)) {
    values <- config$filters[[col]]
    
    if (col == "station_name") {
      deployments <- deployments %>%
        dplyr::filter(stringr::str_detect(.data[[col]], 
                                          stringr::regex(paste(values, collapse = "|"), ignore_case = TRUE)))
    } else {
      deployments <- deployments %>%
        dplyr::filter(.data[[col]] %in% values)
    }
  }
  
  deployments <- deployments %>%
    dplyr::distinct(deploy_date_time, .keep_all = TRUE)
  
  # ----------------------------------------------------------------------------
  # write output
  write.csv(deployments, output_csv_path, row.names = FALSE)
  
  message("CSV written to: ", output_csv_path)
}

# ------------------------------------------------------------------------------
# allow command-line execution
args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 1) {
  run_etn_pipeline(args[1])
}