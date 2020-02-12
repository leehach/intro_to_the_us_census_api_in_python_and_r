## ------------------------------------------------------------------------
library(tidyverse)
library(tidycensus)
# census_api_key("REPLACE_WITH_YOUR_CENSUS_API_KEY", install = TRUE) 

states = get_acs(
  geography = "state",
  variables = c("B19013_001"),
  year = 2018,
  output = "wide",
  geometry = FALSE
)

head(states)

## ------------------------------------------------------------------------
states = states %>% rename(state = GEOID, name = NAME, mhi = B19013_001E, mhi_moe = B19013_001M)


## ------------------------------------------------------------------------
head(states)


## ------------------------------------------------------------------------
library(sf)
options(tigris_use_cache = TRUE)

# Rerun with geometry = TRUE
states = get_acs(
  geography = "state",
  variables = c("B19013_001"),
  year = 2018,
  output = "wide",
  geometry = TRUE
) %>% rename(state = GEOID, name = NAME, mhi = B19013_001E, mhi_moe = B19013_001M)



## ------------------------------------------------------------------------
library(tmap)
# class(states)

tm_shape(states) +
  tm_polygons(col = "mhi")


## ------------------------------------------------------------------------
states %>% filter(!name %in% c("Alaska", "Hawaii", "Puerto Rico")) %>%
  tm_shape(projection = "laea_NA") +
  tm_polygons(col = "mhi")


## ------------------------------------------------------------------------
pa_counties = get_acs(
  geography = "county",
  table = "B28010",
  year = 2018,
  output = "wide",
  state = "Pennsylvania",
  geometry = TRUE
)
head(pa_counties)


## ------------------------------------------------------------------------
pa_counties = pa_counties %>% mutate(pct_has_computer = 100 * B28010_002E / B28010_001E)
pa_counties = pa_counties %>% st_transform(crs = 2272)

tm_shape(pa_counties) +
  tm_polygons(col = "pct_has_computer", palette = "YlGnBu")

