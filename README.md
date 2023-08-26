# Signlingo-Steamhack2023
 ## How to run the website
Clone github repository by pasting this line into your device terminal
```
git clone https://github.com/tom1209-netizen/Signlingo-Website.git
```
Move to cloned directory
```
cd Signlingo-Website
```
Create an virtual enviroment 
```
python -m venv <name_of_virtualenv>
```
Activate the enviroment  
**Note that you have to use different code depending on your device os**  

For **Macos** use  

```
source <name_of_virtualenv>/bin/activate
```
For **Windows** use
```
source <name_of_virtualenv>\Scripts\activate
```

Install all neccessary libraries
```
pip install -r requirements.txt  
```

Run the server backend flask python
```
flask run
```

# Model
Accuracy on test set: 90%
Loss on test set: 33%
## Model architecture

![](https://hackmd.io/_uploads/ryA1cUw63.png)

## Visualize accuracy and loss

![](https://hackmd.io/_uploads/r12tBwwTn.png)


## Confusion matrix

![](https://hackmd.io/_uploads/ryVmSvvTn.png)
