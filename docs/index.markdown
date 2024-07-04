---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults
title: The BxC toolkit
layout: splash
intro:
  - image_path: /assets/images/logo.png
    excerpt:
      BxC, which stands for **magnetic fields** from **multiplicative chaos**, is a swift generator for 3D turbulent magnetic fields, which allows to generate high-resolution data cubes, **in minutes**, on laptops and desktops.

capabilities:
  - image_path: /assets/images/mix.png
    excerpt:
      In addition to having an actual “look-and-feel” resemblance to turbulent fields, BxC-generated fields also match physical turbulent flows in terms of higher order statistics, compared to actual DNS simulations. The relatively simple Python implementation allows for full user-controlled customization of the power spectrum as well as the inclusion of realistic features such as anisotropy and background structured topologies.  
    title: Capabilities    
    url: /features
    btn_label: See more
    btn_class: btn--primary

feature_row:
  - image_path: /assets/images/python.png
    excerpt: 
      BxC is fully implemented in Python. The relatively simple structure of the code makes it extremely user-friendly and easy to use. The Python implementation also facilitates the post-processing of data, for which users can readily use their own routines. 
    title: Getting started
    url: /user_guide
    btn_label: User Guide
    btn_class: btn--primary

  - image_path: /assets/images/3D.png
    excerpt:
      The development of BxC took and still takes a lot of time and effort. We kindly ask that the first published peer-reviewed paper from applying BxC is done in co-authorship with at least one of the original authors. Additionally, if you use BxC in a publication we kindly request that you cite the code paper.
    title: Using BxC 
    url: /publications
    btn_label: Published works
    btn_class: btn--primary

  - image_path: /assets/images/funds.png
    excerpt: BxC is supported by funding from the European Research Council (ERC) under the European Unions Horizon 2020 research and innovation programme, Grant agreement No. 833251 PROMINENT ERC-ADG 2018; the project received funding from the Internal Funds KU Leuven, Project No. C14/19/089 TRACESpace, and Agence Nationale de la Recherche, project BxB:ANR-17-CE31-0022.
    title: Fundings
    url: https://erc-prominent.github.io/
    btn_label: erc PROMINENT
    btn_class: btn--primary
 
---

{% include feature_row id="intro" type="center" %}

{% include feature_row id="capabilities" type="left" %}

{% include feature_row %}
