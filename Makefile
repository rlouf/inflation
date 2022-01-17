
price_data: data/raw/ap.series \
	data/raw/ap.area \
	data/raw/ap.data.0.Current \
	data/raw/ap.data.1.HouseholdFuels \
	data/raw/ap.data.2.Gasoline \
	data/raw/ap.data.3.Food \
	data/raw/ap.period data/raw/ap.txt

us-prices.db:
	sqlite3 $@ < schema.sql

fetch-price-data: $(DATAFILES)

# Links series ID to area code and item code
data/raw/ap.%:
	mkdir -p $(dir $@)
	wget -c https://download.bls.gov/pub/time.series/ap/$(notdir $@) -O $@
