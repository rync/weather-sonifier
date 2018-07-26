# weather-sonifier
A rudimentary approach to sonifying weather data.

## Why Sonification?
My interest in sonification was inspired by a professor of mine at Penn State University, Mark Ballora.
You can hear him discuss some of his work with data sonification during a [recent TED talk](https://www.youtube.com/watch?v=aQJfQXGbWQ4).

Embedded in data sonification is a premise positioned opposite to that of something like Machine Learning.
Whereas ML suggests there are problems that are beyond the abilities of humans (temporally or otherwise) to complete,
sonification hints that one has the ability to understand more than we generally assume, if only it were presented in the proper format.

This is my first attempt at creating a data sonification project, so it's very rudimentary. At this stage, it is basically a proof-of-concept.

## Pre-Requisites

* Python 3.5 or 3.6
* A couple of packages, which can be installed by running `pip install urllib bs4`
* Install [ChucK](http://chuck.cs.princeton.edu/release/), a strongly-timed audio generation environment created by Ge Wang at Princeton.

## Running the script.

To run the script, in the top directory of the project, simple run `python main.py`. The audio will begin automatically, and can be closed by pressing CTL+C.
By default, the coordinates for the weather location are set to Robinson, PA (40.44, -80.07).

The generated Chuck files will be stored in `./utilities/generatedChuckFiles/`, and are titled based on the time from epoch at which they were generated.

Additionally, latitude and longitude may be set at the command-line, e.g.

`python main.py latitude=40.7146 longitude=-74.0071`

or

`python main.py lat=29.4246 lon=-98.4946`

If this is performed, both latitude _and_ longitude must be provided, and they must be located within the United States.

## Future Plans

Obviously, this is an extremely rudimentary Proof of Concept, but future development could involve the following:
* Refactoring utility classes into proper classes when possible
* Stability improvemnts to account for missing values, common on the NOAA site for many locations
* Melody Generation
* Scaling of readings based on regional averages and using more effect tools, such as pandas
* Utilizing an actual API over webscraping
* Account for Dew Point => Frost Point conversion
* Setting up a Jenkins job on a server to crossfade between previous and current regenerations at set intervals
* Hazardous Weather Warnings
* Reacting Sunrise/set, Moonrise/set, and Twilight
* Interpreting Current Conditions strings (e.g. Cloudy, Overcast, etc.)
* Ambient light control via LED's (possibly platform specific for a Raspberry Pi or other dev computer)