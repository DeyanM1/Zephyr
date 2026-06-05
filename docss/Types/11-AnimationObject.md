# Animation Object


a animation Object is used to render Frames inside of the terminal.


```Zephyr

ao # AO:<*- initialFrame>|<*- delayInSeconds>|<*- clearScreen>; § initialFrame is either PT or list of PT; delayInSeconds is the delay between the displayed frames; clearScreen enables if the screen should be cleared after each frame: allowed values: ~0/~1
ao ? w:<*FrameToAdd>;                            § adds a frame to the current animation. Accepts any Type that can convert to PT
ao ? setDelay:<*seconds>;                        § sets the delay of the automatic animation: accepty INT
ao ? clearScreen:<*bool>;                        § clear the screen between frames. accepts: ~1/~0
ao ? setIndex:<*index>;                          § value to set the current index to. prints the frame at the position. accepts INT
ao ? start:;                                     § starts the animation from the current index. after finish it restarts the index to 0
ao ? step:;                                      § steps a index forward and prints the frame
ao ? display:;                                   § displays the frame without incrementing the index
ao ? reset:;                                     § resets the index to 0 without printing any frames

```
