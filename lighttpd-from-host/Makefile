.PHONY: module clean

SRC = $(shell readlink -f ../..)

lighttpd_path = $(shell realpath $$(which lighttpd))

ifneq "$(wildcard /usr/lib64/lighttpd)" ""
lighttpd_lib_path = /usr/lib64/lighttpd
else
lighttpd_lib_path = /usr/lib/lighttpd
endif

module: data
	$(SRC)/scripts/manifest_from_host.sh $(lighttpd_path) > usr.manifest
	echo '/www-data/**: $${MODULE_DIR}/www-data/**' >> usr.manifest
	echo '/lighttpd.conf: $${MODULE_DIR}/lighttpd.conf' >> usr.manifest
	echo '/lighttpd-nfs.conf: $${MODULE_DIR}/lighttpd-nfs.conf' >> usr.manifest
	echo '/lighttpd-virtiofs.conf: $${MODULE_DIR}/lighttpd-virtiofs.conf' >> usr.manifest
	@if [ -d $(lighttpd_lib_path) ]; then echo '/usr/lib/lighttpd/**: $(lighttpd_lib_path)/**' >> usr.manifest; else echo 'ERROR: Failed to find lighttpd libraries'; fi

data targets:	# NOTE: These can be generated independently, but they are semantically coupled
	mkdir -p data
	truncate -s 0 targets
	bash -c 'RANDOM=1; for i in {1..10}; do r=$$((RANDOM / 2 + 1)); yes | head -c $${r}K > data/$${i}; echo "GET http://192.168.122.15/$${i}" >> targets; done'

clean:
	rm -rf usr.manifest data targets
