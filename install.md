---
layout: page
title: userguide
---

{% include JB/setup %}


{% capture subhead %}
  <h1>Try Compass</h1>
  <p class="lead">Compass Appliance - An Illustration of Compass Magic</p>
{% endcapture %}


{% capture sidebar %}

<ul class="nav nav-list bs-docs-sidenav">
  <li class="active"><a href="#introduction">Introduction</a></li>
  <li><a href="#step-one">Step 1 - Install Compass</a></li>
  <li><a href="#step-two">Step 2 - Compass-Web</a></li>
  <li><a href="#step-three">Step 3 - Discover Machines</a></li>
  <li><a href="#step-four">Step 4 - Security</a></li>
  <li><a href="#step-five">Step 5 - Networking</a></li>
  <li><a href="#step-six">Step 6 - Hosts</a></li>
  <li><a href="#step-seven">Step 7 - Review and Deploy</a></li>
  <li><a href="#step-eigth">Step 8 - Start hosts</a></li>
  <li><a href="#step-nine">Step 9 - OpenStack</a></li>
  <li><a href="#appendix1">Appendix I - Ubuntu</a></li>
  <li><a href="#appendix2">Appendix II - FAQ</a></li>
</ul>

{% endcapture %}


{% capture maincontent %}

  {% include /installguides/introduction.md %}
  {% include /installguides/step1.md %}
  {% include /installguides/step2.md %}
  {% include /installguides/step3.md %}
  {% include /installguides/step4.md %}
  {% include /installguides/step5.md %}
  {% include /installguides/step6.md %}
  {% include /installguides/step7.md %}
  {% include /installguides/step8.md %}
  {% include /installguides/step9.md %}
  {% include /installguides/appendix1.md %}
  {% include /installguides/appendix2.md %}

{% endcapture %}

{% include /userguides/template.html %}

