## docker_helpers ##

This project contains python helper scripts to run a docker image associated with TOPMed.  The project includes the following helper scripts:
1. analysis_pipeline.py
2. ap_analysis.py
3. Rdocker.py
4. Rstudio_docker.py

These python scripts provide common features including:
1. Script help (<i>**--help**</i>)
2. Running a specified docker image (default: <i>**uwgac/topmed-rstudio**</i>)
2. Bind-mounting of local working directory to docker  (docker run option <i>**-v**</i>)
3. Passing command and command arguments to the docker image
4. Running the docker image with appropriate options and command arguments

#### analysis_pipeline.py ####
Execute analysis pipeline (e.g., <i>grm</i>) on AWS batch. The general command syntax is:
```{r}
analysis_pipeline.py -a <analysis pipeline> -p <pipeline parameters> [options]
```
Execute <i>analysis_pipeline.py --help</i> for more details.

<i>Examples</i>

#### ap_analysis.py ####
Execute interactively an analysis stage in an analysis pipeline (which is useful for debugging or testing).  The general command syntax is:
```{r}
ap_analysis.py -a <analysis> -p <analysis parameters> [options]
```
Execute <i>ap_analysis.py --help</i> for more details.

<i>Examples</i>
#### Rdocker.py ####
Run R interactively by creating a docker container (default named <i>Rdocker</i>) and running R interactively.  

The characteristics and attributes of the R session includes:
1. When R initially starts up, the current working directory in the container is <i>/home/rstudio</i>
2. By default, the current working directory on the local computer is mapped to the container's working directory of R
3. Optionally, an additional data folder on the local computer can be mapped into the container (<i>-d</i> option)
3. Optionally, the container can persist (<i>-k</i> option) and re-executed (<i>-e</i> option).

The general command syntax is:
```{r}
Rdocker.py [options]
```
Execute <i>Rdocker.py --help</i> for more details.

<i>Examples</i>
1. <i>Example 1</i>
```{r}
Rdocker.py
```
Example 1 runs R interactively in a container named <i>Rdocker</i>.  The current working directory in the local computer is mapped to <i>/home/rstudio</i>.

2. <i>Example 2</i>
```{r}
Rdocker.py -d /projects/topmed:/data
```
Example 2 runs R interactively in a container named <i>Rdocker</i>.  The current working directory in the local computer is mapped to <i>/home/rstudio</i> and the local directory <i>/projects/topmed</i> is mapped in the container to <i>/data</i>.

#### Rstudio_docker.py ####
Run Rstudio server within a docker container in the background (or detached).  This enables a browser on a local computer to start an Rstudio session.

The Rstudio session has the following characteristics and attributes:
1. The user name and password is <i>rstudio</i>
2. The current working directory of the Rstudio session is <i>/home/rstudio</i>
3. By default the current working directory in the Rstudio session is mapped to the current working directory of the local computer

The general command syntax is:
```{r}
Rstudio_docker.py [options]
```
Execute <i>Rstudio_docker.py --help</i> for more details.

<i>Examples</i>
1. <i>Example 1</i>
```{r}
Rstudio_docker.py
```
The example above runs Rstudio server in the background in the container named <i>rstudio</i>.  In the local computer's browser, the following URL will create an Rstudio session:
```{r}
localhost:8787/
```
2. <i>Example 2</i>
```{r}
Rstudio_docker.py -i 192.168.1.4 -p 8080
```
The example above runs Rstudio server in the background in the container named <i>rstudio</i>.  In a local computer's browser, the following URL will create an Rstudio session:
```{r}
192.168.1.4:8080/
```
3. <i>Example 3</i>
```{r}
Rstudio_docker.py -C kill
```
The example above kills the background docker container named <i>rstudio</i>