PY			= python
VENV		= .venv
MODULE		= mazegen
WHL			= $(MODULE)-1.0.0-py3-none-any.whl

CLEARLINE	= \r\033[K
RESET		= \e[0m
BOLD		= \e[1m
RED			= \e[31m
GREEN		= \e[32m
YELLOW		= \e[33m
CYAN		= \e[36m
WHITE		= \e[37m
GREY		= \e[90m

define head
$(BOLD)$(GREY)[$(2)$(1)$(GREY)]$(RESET)
endef

HEAD_INFO		= $(call head,INFO,$(CYAN))
HEAD_SUCCESS	= $(call head,SUCCESS,$(GREEN))
HEAD_ERROR		= $(call head,ERROR,$(RED))

define step
	@printf "$(HEAD_INFO) $(1)..."; \
	out="$$( { $(2); } 2>&1 )"; \
	status="$$?"; \
	if [ "$$status" -eq 0 ]; then \
		printf "$(CLEARLINE)$(HEAD_SUCCESS) $(1)\n"; \
	else \
		printf "$(CLEARLINE)$(HEAD_ERROR) $(1)\n"; \
		printf "\n$$out\n\n"; \
		exit $$status; \
	fi
endef

define exec
	@printf "$(HEAD_INFO) $(1)...\n"; \
	$(2); \
	status="$$?"; \
	if [ "$$status" -eq 0 ]; then \
		printf "$(HEAD_SUCCESS) $(1)\n\n"; \
	else \
		printf "$(HEAD_ERROR) $(1)\n\n"; \
		exit $$status; \
	fi
endef

define log
	@printf "$(1) $(2)\n";
endef

all: install run

install:
	$(call exec,Installing requirements,$(PY) -m pip install -e .[dev])

run:
	$(call exec,Running main script,$(PY) a_maze_ing.py config.txt)

debug:
	$(call exec,Running main script in debug mode,$(PY) -m pdb a_maze_ing.py config.txt)

clean:
	$(call step,Removing __pycache__,rm -dfr $(shell find . -name '__pycache__'))
	$(call step,Removing .mypy_cache,rm -dfr $(shell find . -name '.mypy_cache'))
	$(call step,Removing .pytest_cache,rm -dfr $(shell find . -name '.pytest_cache'))
	$(call step,Removing .egg-info, rm -dfr $(shell find . -name '*.egg-info'))
	$(call step,Removing dist folder,rm -dfr dist)

lint:
	$(call step,Checking Norm,$(PY) -m flake8 .)
	$(call step,Checking Typing,$(PY) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs)

lint-strict:
	$(call step,Checking Norm,$(PY) -m flake8 .)
	$(call step,Checking Typing,$(PY) -m mypy . --strict)

test:
	$(call exec,Running tests,$(PY) -m pytest)

venv:
	$(call step,Creating Python Environment,python3 -m venv $(VENV))
	$(call log,$(HEAD_INFO),Run $(YELLOW)source $(VENV)/bin/activate$(RESET) to enter the environment and $(YELLOW)source ~/.zshrc$(RESET) to leave it)

build: dist/$(WHL)

dist:
	$(call step,Creating dist folder,mkdir dist)

dist/$(WHL):
	$(call exec,Building the module,$(PY) -m build)

install-$(MODULE): dist/$(WHL)
	$(call exec,Installing the module,cd dist && $(PY) -m pip install $(WHL))

uninstall-$(MODULE): dist
	$(call exec,Uninstalling the module,cd dist && $(PY) -m pip uninstall mazegen -y)

.PHONY: all install run debug clean lint lint-strict test venv build install-$(MODULE) uninstall-$(MODULE)
