# User config
configfile: "showyourwork.yml"


# Import the showyourwork module
module showyourwork:
    snakefile:
        "showyourwork/workflow/Snakefile"
    config:
        config


# Use all default rules
use rule * from showyourwork

rule affiliated_registry:
    input:
        "src/scripts/affiliated-registry.py"
    output:
        "src/generated/affiliated-table.tex"
    conda:
        "environment.yml"
    shell:
        "python {input[0]}"

rule git_header:
    input:
        "src/scripts/make-repo-info.py"
    output:
        "src/generated/git-header.tex"
    conda:
        "environment.yml"
    shell:
        "python {input[0]}"
