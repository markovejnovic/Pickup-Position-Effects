# Pickup-Position-Effects

The following is a small research paper investigating the effects of pickup 
position on harmonics in an electric guitar. It consists of the LaTeX documents
and the code for processing the data. The data is included as well.

## Raw data

You can find the raw data in `src/Data`.

## Data processing

Every piece of data processing is done in `python`.

### Requirements

You need `matplotlib`, `numpy`, `scipy`.

### Getting started

To give the algorithm a spin, clone the repository:
```bash
git clone git@github.com:markovejnovic/Pickup-Position-Effects.git
```
Next, add execution privileges to the script
```bash
cd Pickup-Position-Effects
chmod +x ./src/boiler.py
```

You can use the samples provided in the directory to test the algorithm.
```bash
./src/boiler.py ./src/Data
```

There are several options you can pass to the boiler program:
```bash
-c Connects the scatter plots with line plots (connects harmonic peaks)
-e Draws the line of expected fit
-p Plots the scatter plot
```
These can be used in unison, so `./src/boiler.py -p -c ./src/Data` will plot a 
3D scatter plot and try to connect the peaks of the harmonics together.

## Acknowledgments

* Just [PurpleBooth](https://github.com/PurpleBooth) for showing me how to make a [good README.md](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2) file.



