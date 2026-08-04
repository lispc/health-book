EPUB = dist/健康生活全书.epub
SRCS = $(sort $(wildcard book/*.md))

epub: $(EPUB)

$(EPUB): $(SRCS)
	mkdir -p dist
	for f in $(SRCS); do sed '/^<!-- chapter-nav -->$$/,$$d' "$$f"; echo; done | pandoc -f markdown -o $@ \
		--metadata title="健康生活全书" \
		--metadata author="张卓" \
		--metadata lang=zh-CN \
		--toc --toc-depth=1
	@echo "生成完成：$(EPUB)"

nav:
	python3 scripts/add_nav.py

clean:
	rm -f $(EPUB)

.PHONY: epub nav clean
