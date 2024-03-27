# Simple CPU Management GUI
This app is my really first app written in Python!
I work and play on laptop, so I need to control my CPU frequency to avoid unnecessary overheating. On Windows, I usually do that through [ThrottleStop](https://www.techpowerup.com/download/techpowerup-throttlestop/), but now I use a Linux distribution as my primary OS. When I discovered and started to use *cpupower*, I thought of creating a GUI to easily change governor policy and frequency! After some time, here it is!

## Usage
Pretty straightforward: launch the executable, change what you want to, and click on the corresponding button to validate your choices. 
Because the `cpupower frequency-set` command need root privileges, you'll be prompt to enter your password each time you click on a button (nothing is stored, it acts like when you do it directly via a terminal).

## Notes
Feel free to tell me if I can improve this app, or if you have bugs or suggestions!
