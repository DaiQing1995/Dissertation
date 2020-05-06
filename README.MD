# Dissertation

Generate tags for Docker container by analyzing the description of Docker Container.
Implemented by python, mysql is used as database.

## Method Intro
Four methods in the mechanism of tags generation,  files and folders' description are shown as followed.

method:
+ cluster: hierarchical clustering for general tag generation
+ LDAtag: LDA based method
+ tagextend: Vertical tag generation
+ wordnet_extend: Horizontal tag generation

plain classes:
+ entity: for document use
+ data: the source data obtained from DockerHub

utils:
+ preprocessing: data preprocess

main.py: the entrypoint of method with functions of each four methods. Check it when using.

## Related Project

1. Data Obtaining based on C : https://github.com/DaiQing1995/Docker-Hub-Crawler

2. Manual evaluation baesd on Java, a B-S software:  https://github.com/DaiQing1995/GeneratedTagManualEvaluation