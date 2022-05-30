# Multi-label Classification of Movies :film_projector:

# Abstract

This paper approaches the problem of multi-label classification of
images, for the specific case of movie posters. Since a genre is quite
an abstract concept, it is interesting to investigate if and how
features of genres could be captured in the poster of the movie; and
with what accuracy the different genres could be predicted. The problem
was approached by using a modified DenseNet architecture, resulting in
an average accuracy of 26.41%. The genres of movie posters with distinct
features could be classified quite well whilst movie posters containing
elements of multiple genres were more difficult to classify.

# Introduction

Image classification is used for many applications, including everything
from analysis of medical images for diagnosing illnesses to
recommendation systems working on images. The problems including image
classification can be approached in many ways, where everything from
data set, network architecture, the model used, as well as hyper
parameters and several other factors play into the result of the work.
The difficulty lies in finding the most suitable combination for the
problem at hand.  
One application of image classification, the one explored in this
project, is the ability to classify a movie genre based on it’s poster.
The concept of genres are quite abstract, in the way that humans
understand them. Not only is it difficult to pinpoint the exact
characteristics of a certain genre, but it is also an interesting
question whether an abstract concept like a genre can be captured in an
image. To make the classification more difficult, a movie can belong to
multiple genres with no such correlation among them, making it a
multi-label classification problem.  
There are many approaches to solve this type of problem, and several
have been studied prior to this project. In one paper, a multi-genre
classification was conducted, by a comparison between the performance of
three different architectures; ResNet-50, VGG-16 and DenseNet-169. They
found that the DenseNet-169 had the best performance out of the three,
and suggested that improvements could probably be achieved through using
object identifier algorithms such as YOLO mentioned in [5.3](#obj),
finding better data or using other architectures.  
Contributions of this work are summarized as follows:

  - Clean and transform movie poster dataset along with metadata like
    movie director, actor, imdb rating etc. for the years 1980-2015.
    Perform image augmentation to the movie posters for genres which are
    under represented, see [3.1](#data).

  - Construct and train a deep neural network to classify the movie
    posters into multiple genres with each image from the dataset having
    multiple labels. [3.2](#system)

  - Compare the results of different genres and derive insights on what
    makes a genre easier or difficult to predict, mentioned in
    [4](#result) and [4.2](#discuss).

  - Compare and contrast custom convolutional neural network with a
    modified version of pretrained deep neural networks like DenseNet,
    see [4.2](#discuss).

# Theory

## DenseNet-121

Densely Connected Convolutional Networks (DenseNets)  attempt to solve
the problem of information passed through a deep network vanishing by
the time of reaching the network’s last layers. The idea is to therefore
connect early layers to later layers. DenseNets connect all layers
directly with each other and combine features passed to a layer through
concatenation.  
The three-dimensional RGB images are initially passed through a sequence
of a convolutional layer, a batch normalization layer, a ReLU and a
pooling layer. Their output is propagated through a network of four
dense blocks which are connected through transition layers. A dense
block contains a sequence of dense layers which consist of a batch
normalization layer, a ReLU and a convolutional layer. A transition
layer consists of a batch normalization layer and ReLU followed by a
convolutional and pooling layer. In the end, the output data of 1024
vector is passed through a fully connecting layer with a softmax
function.

# Method

## Data

The data set used consists of 8052 movies, with their poster images and
some additional metadata for each movie like imdb rating, director,
actors, run time and so on. Every movie is labelled by at least one of
28 different genres present in the data set with number of genres
ranging from 1 to 3, for example `Drama` and `Action`. A full list is
included in [7](#appendix:A).

Most movies have more than one genre. As the data set is too small to
train on a deep neural network, and some genres being under represented,
there was a need to augment the data and combine the genres that have
very few images. The genres `Adult`, `Game-Show`, `News`, `Reality-TV`,
`Short`, `Talk-Show` and `Western` were combined under `Other`-genre
category. The two genres `Music` and `Musical` were also combined into
one, giving out 20 genres to work with. To achieve a balanced set,
images were augmented to get 3000 samples per genre by randomly cropping
them of size 150x150. Since one image can have multiple labels,
augmenting one image meant increasing the samples of that image for all
its corresponding labels. To tackle this issue, the images were not
augmented if they had already been augmented for some other genre. This
resulted in total of 26049 images as our final input to be trained and
tested. The 20 genres are multi-hot encoded and fed into the models.
Refer to Figure [\[appendix:before\_aug\]](#appendix:before_aug) and
[2](#fig:after_aug) for the genre-wise breakdown of images before and
after augmentation.

![Before Augmentation](report_imgs/before_augmentation.png?raw=true "Before Augmentation")

![After Augmentation](report_imgs/after_agumentation.png?raw=true "After Augmentation")

## System Design :jigsaw:

### Modified DenseNet-121

The system consists of a modified DenseNet121 architecture. The
multilayered perceptron at the end of the convolutional layer is now
consisting of 1024 input features, with sigmoid activation function
instead of softwax function since we have the model has to predict
values for a multi-label problem. It gives out a prediction score vector
representing 20 genres.  

![DenseNet121 Model](report_imgs/densenet.drawio.png?raw=true "DenseNet121 Model")  
DenseNet121 Model  

The loss function used is binary cross entropy. The system furthermore
uses the Adam optimizer to alter the learning rate while doing gradient
descent. The model is trained on 70% of the data, i.e. 18234 images, and
tested on the remaining 7815 images.

### Custom Convolutional Neural Network

A Custom CNN model was also trained on the same dataset. The model
consisted of 6 convolutional layers each followed by pooling layers,
dropout layers and ReLU as an activation function. The fully connected
layer is then attached with a sigmoid function giving out a prediction
score for 20 genres.

![Custom CNN](report_imgs/densenet-Page-2.drawio%20(1).png?raw=true)  
Custom CNN  

# Results

## Model Accuracy :dart:

The accuracy of a model is measured by taking the ratio of top *n*
predicted scores to the number of genres in the ground truth, where is
*n* is the number of genres in the ground truth. If a movie, for
instance, is labeled with two genres, the top 2 predictions are
considered as the model’s output and compared with the ground truth.
Then, if one of the two ground truth labels is in the model’s top 2
predictions, the accuracy is said to be 50% for this poster as one genre
was predicted correctly and the other was not. If both ground truth
labels are predicted by the model, the accuracy is said to be 100%. The
mean accuracy is measured over a test set of 7815 movie posters after
each training epoch.  
The hyperparameters used for both DenseNet and Custom CNN models were
same which included the mini-batch size as 2, learning rate as 0.5,
number of epochs as 10, training size 70% of the whole dataset. The
Binary Cross entropy loss function and the Adam optimizer were used with
the default parameters as provided by pytorch library.

<div id="tab:res:mip">

|      Model | Average accuracy |
| ---------: | ---------------: |
|   DenseNet |           26.41% |
| Custom CNN |             4.1% |

Average accuracy for the different models over all epochs. 

</div>

  
Figure [\[fig:jonny\_english\]](#fig:jonny_english) and
[\[fig:gladiator\]](#fig:gladiator) shows that the DenseNet classified
the movies correctly. Figure [7](#fig:shangai_story) was misclassified
perhaps due to the dark features in the image which was generalized as
being ’Crime’ and ’Drama’ by the model.

![  
Predicted value: Crime, Drama  
Ground truth: Comedy, Drama](report_imgs/jonny%20english_github.png?raw=true)  
Predicted value: Crime, Drama  | Ground truth: Comedy, Drama  

![  
Predicted value: Crime, Drama  
Ground truth: Comedy, Drama](report_imgs/Gladiator_github.png?raw=true)  
Predicted value: Crime, Drama | Ground truth: Comedy, Drama  

![  
Predicted value: Crime, Drama  
Ground truth: Comedy, Drama](report_imgs/shanghai_story_github.jpg?raw=true)  
Predicted value: Crime, Drama | Ground truth: Comedy, Drama  

## Discussion

Any classification problems’ accuracy depends on how well the different
classes are separated from each other. In the case of movie poster
classification based on genre; there are several challenges to consider.
Firstly, as mentioned previously in this report, the genre concept is
quite abstract and not necessarily easy to distinctly define features of
in an image. Figure [8](#fig:carter_high) is one such example which
shows that a human might classify a poster like this to be in ’Sports’
genre, but instead it belongs to ’Crime’ and ’Drama’, which was
correctly identified by the model because of its dark features.

![Predicted value: Crime, Drama  
Ground truth: Crime, Drama](report_imgs/carter_high_github.jpg?raw=true)  
Predicted value: Crime, Drama | Ground truth: Crime, Drama  

Secondly, most of our data set examples include several labels of
different genres, of course in different combinations with each other.
It is very possible that these genres are not equally represented in the
movie posters. Thirdly, the number of genres will impact our prediction
accuracy, where more classes lead to a more difficult problem.  
Another thing to take into consideration is the data set we used, which
is quite small in relation to the number of genres. Since the data set
is small, we use random augmentation to increase the size; it is also
possible that this random augmenting can impact the performance since
different cropping of images could result in different representations
of the genres.  
One problem observed with the predictions is that some of the genres are
not predicted at all. This of course contributes to wrong predictions,
since all genres are indeed represented in the data set. One possible
reason for this lies in the augmentation of the data set. When going
through the data set, we aim to make the under represented genres
bigger. However, it’s possible that the overlap of genres makes our
approach insufficient. Consider two genres with a big overlap. If one of
the genres have close to 3000 examples (which was our set value), it
will barely be augmented. Let’s say the other overlapping genre is much
smaller, so it should be augmented to maybe 5 times it’s original size,
but since the first genre has already "augmented" the movies existing in
both genres, the smaller set is barely augmented either.  
Since we have 20 genres, the average accuracy of a random classification
for a movie with a single genre would be \(5\%\). For additional genres,
the accuracy would of course be much lower, two genres already resulting
in \(0.25\%\) and three genres in \(0,0125\%\). Considering this, and
the fact that on an average the number of genres lied between 2 and 3,
the model results can be considered to be better than a random
classifier.  

# Related work

The following work presented is in some way related to our work, in the
case of [5.2](#att) and [5.3](#obj), they are two promising methods that
could be used to enhance the performance of image classification.

## Genre classification

The problem of genre classification has been approached in numerous
studies, for example music genre classification, art classification, and
movie genre classification based on other things than posters, like
classification based on the trailer of a movie. There is even examples
of classification of emotions present in music. All of these tasks have
similarities with the task of classifying a movie poster into a genre.
However, there are also several differences. For example, a movie
trailer is essentially a large number of pictures combined into a
sequence, combined with audio. Considering that compared to our task,
classifying a movie based on a single image, the data to use for the
classification of a trailer is significantly richer.

## Attention methods

One paper, also on the subject of movie genre classification, uses an
attention mechanism to solve the problem. Attention mechanisms are used
to select input subsets to process, and can be used in neural networks
to weight features extracted and in that way create a context of which
parts of the input should be emphasized. The proposed method of the
paper was to use what is called a Gram layer in a convolutional neural
network. First it extracts style features and produces a feature map of
a poster image. Next, style weights are extracted which are multiplied
by the input tensor, thus working as an attention mechanism during
classification. Attention methods seem to have the potential to improve
classification where different style elements can be captured for the
different classes.

## Object detection

In another paper on movie genre classification , one of the suggested
approaches mentioned in [1](#intro) is used; the writers of the paper
combined the outputs of a regular CNN with the output of object
identification using YOLO, giving a multi-genre output. In their work,
they tried in total 7 approaches to the same problem, coming to the
conclusion that the combined object detection approach was the most
successful.  
Object detection is a well-studied part of the image processing-field
due to its many and highly relevant applications. The specific method
used in mentioned paper is YOLO.

YOLO stands for `You only look once`, and as the name suggests, an image
is processed in one single network and during one evaluation using YOLO.
YOLO divides the image into bounding boxes and predicts the
probabilities of object classes within those boxes. Due to its simpler
architecture, YOLO is faster than for example another popular method
called Faster R-CNN, and achieves very general representations of
objects, which means that it can perform quite well even to data that is
quite different from the data it’s been trained on. However, YOLO
struggles to identify certain things, for example small objects in
groups.  
When using object detection, there is the option of using pre-trained
models or training a model yourself based of the objects present in
movie posters specifically, as it may vary to the objects that can be
detected by general models. Depending on your data set, the object
detection might also be more or less useful, as in our case we crop the
images randomly, and risk cropping the objects up making it less
relevant. However, object detection seems to be able to greatly improve
prediction in applications similar to our problem at hand.

# Conclusion and future work

Predicting movie genres based on the movie’s poster is difficult based
on a range of factors. Since a movie can have multiple genres, features
of a movie poster cannot be distinguished as such. Movie posters
belonging to different genres can have similar features and one movie
poster can simultaneously contain features typical to different
genres.  
To improve the genre prediction, a larger and adequately balanced data
set should be retrieved to train the model on. The choice of genres to
classify might also improve the results since certain genres may be more
difficult to classify. Furthermore, the system could be extended with an
object detection model, so that a consecutive model can learn which
objects are commonly represented on movie posters from a certain genre.
Since many movie posters depict people, the model could be trained on
different characters and their expressions.

# Genre list

  - Action

  - Adventure

  - Animation

  - Biography

  - Comedy

  - Crime

  - Documentary

  - Drama

  - Family

  - Fantasy

  - History

  - Horror

  - Music

  - Mystery

  - Romance

  - Sci-Fi

  - Sport

  - Thriller

  - War

  - Other (including Game-Show, News, Reality-TV, Short, Talk-Show,
    Western, Adult)
