VERSION=1.19.2
SOURCE=http://nginx.org/download/nginx-${VERSION}.tar.gz
CONFIGURE_MODULES=--prefix=/nginx/ --with-debug --without-http_rewrite_module --with-threads --with-http_stub_status_module

.PHONY: module clean

SRC=upstream/nginx

module: usr.manifest

usr.manifest: $(SRC)/nginx.so data
	echo '[manifest]' > usr.manifest
	echo '/nginx.so: $${MODULE_DIR}/$(SRC)/nginx.so' >> usr.manifest
	echo '/nginx/html/**: $${MODULE_DIR}/upstream/nginx/html/**' >> usr.manifest
	echo '/nginx/logs/**: $${MODULE_DIR}/upstream/nginx/logs/**' >> usr.manifest
	echo '/nginx/conf/**: $${MODULE_DIR}/upstream/nginx/conf/**' >> usr.manifest
	echo '/nginx/conf/nginx.conf: $${MODULE_DIR}/patches/nginx.conf' >> usr.manifest
	echo '/nginx/conf/nginx-nfs.conf: $${MODULE_DIR}/patches/nginx-nfs.conf' >> usr.manifest
	echo '/nginx/conf/nginx-virtiofs.conf: $${MODULE_DIR}/patches/nginx-virtiofs.conf' >> usr.manifest

clean:
	rm -fr upstream data targets
	rm -f upstream.tar usr.manifest

data targets:	# NOTE: These can be generated independently, but they are semantically coupled
	mkdir -p data
	truncate -s 0 targets
	bash -c 'RANDOM=1; for i in {1..10}; do r=$$((RANDOM / 2 + 1)); yes | head -c $${r}K > data/$${i}; echo "GET http://192.168.122.15/$${i}" >> targets; done'

# Note: the touch commands below are needed after commands which create files
# "in the past", like wget and tar, and can confuse Make to rebuild a target
# which is new, just pretends to be old.
upstream.tar:
	wget -c -O $@ $(SOURCE)
	touch $@

$(SRC)/configure: upstream.tar
	mkdir upstream
	tar -C upstream -xf upstream.tar
	cd upstream; ln -sf nginx-${VERSION} nginx
	cd $(SRC); patch -p1 < ../../patches/0001-nginx-OSv-fix-process-spawning.patch
	mkdir $(SRC)/logs; touch $(SRC)/logs/dummy-file
	touch $(SRC)/configure

$(SRC)/Makefile: $(SRC)/configure
	cd $(SRC); ./configure $(CONFIGURE_MODULES) --with-cc-opt='-O2 -D_FORTIFY_SOURCE=2 -fPIC' --with-ld-opt='-pie'

$(SRC)/nginx.so: $(SRC)/Makefile
	$(MAKE) -C $(SRC)
	mv $(SRC)/objs/nginx $(SRC)/nginx.so

.DELETE_ON_ERROR:
