# **Multi-Track PF**
*Tracking multiple objects with systematic re-sampling particle filtering*

<p><img src="images/tracking.gif" alt="foo"title="title" /></p>


As with so many useful or beneficial innovations encountered in life, once I see a simplified example in action, I become confident that I can adapt it to a problem that I'm trying to solve. Often when I need to track objects in video, the object can be detected based on pixel intensities, local structure, learned features, etc. For example, in the case of an unresolved object, it might appear in an sensor's image as only a small blob, but it can be detected by its disc-like shape, or the relative high intensity of the pixels in the disk region. However, there are some cases when we would like to note the presence of the object at an even greater distance, when the signal-to-noise is so low that our eyes might even overlook it if we did not know just where in the image to look.
 
![Alt text](images/closeup.png?raw=true "Output")

