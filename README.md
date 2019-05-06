# conference-paper-rss

## Usage

This is a simple repo for improving conference paper reading experience. We try to parse the paper information(title, abstract, url) of all the papers for a certain conference and generate an rss xml file.
You can use **any RSS reader** to subscribe our resource. In Mac, we recommend using [Leaf](https://itunes.apple.com/cn/app/leaf-rss-%E6%96%B0%E9%97%BB%E9%98%85%E8%AF%BB%E5%99%A8/id576338668?mt=12), which should look like follows:

![leaf-sub.gif](leaf-sub.gif)
![rss-example.gif](rss-example.gif)
### rss source
Use any rss reading client (Leaf in Mac) to subscribe to the following rss resource.
> Currently, we parse papers from the most recent 2 years. earlier years are not included (but you can run our code to parse it by yourself).
+ NIPS:
  + https://conference-paper-rss.github.io/rss_source/nips2018.xml
  + https://conference-paper-rss.github.io/rss_source/nips2017.xml
+ ICML:
  + https://conference-paper-rss.github.io/rss_source/icml2018.xml
+ ICLR:
  + https://conference-paper-rss.github.io/rss_source/iclr2019.xml
  + https://conference-paper-rss.github.io/rss_source/iclr2018.xml
+ CVPR (**note that cvpr2019 has not released official paperlist**):
  + https://conference-paper-rss.github.io/rss_source/cvpr2018.xml
  + https://conference-paper-rss.github.io/rss_source/cvpr2017.xml
+ ECCV:
  + https://conference-paper-rss.github.io/rss_source/eccv2018.xml
+ ICCV:
  + https://conference-paper-rss.github.io/rss_source/iccv2017.xml

## Update (Plan)

* [x] the support of rss source for cvpr (iccv), eccv, ICML, ICLR will be added recently.
  * [x] cvpr(iccv, eccv);  \[update: 2019/05/06\].
  * [x] ICML
  * [x] ICLR
* [ ] a wiki page for usage.
* [ ] the support of generating pdf file instead of xml file will be added recently.
* [ ] the support of ACL, AAAI, ICJAI, KDD and other top conferences (would need to parse dblp), will be added after 1 and 2.
* [ ] a simple webpage would also be considered if this repo is still alive then.


## Other

1. call for new name (the title `conference-paper-rss' is not very attractive).
2. call for proposals (any suggestion for new conference, or other interesting functions.)
