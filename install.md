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
  <li><a href="#get_start">Getting Start</a></li>
  <li><a href="#step-one">Step 1 - Install Compass</a></li>
  <li><a href="#step-two">Step 2 - Compass Web</a></li>
  <li><a href="#step-three">Step 3 - Create Cluster</a></li>
  <li><a href="#step-four">Step 4 - Discover Servers</a></li>
  <li><a href="#step-five">Step 5 - OS Global Config</a></li>
  <li><a href="#step-six">Step 6 - Network</a></li>
  <li><a href="#step-seven">Step 7 - Partition</a></li>
  <li><a href="#step-eigth">Step 8 - Security</a></li>
  <li><a href="#step-nine">Step 9 - Role Assignment</a></li>
  <li><a href="#step-ten">Step 10 - Network Mapping</a></li>
  <li><a href="#step-eleven">Step 11 - Review and Deployment</a></li>
  <li><a href="#step-twelve">Step 12 - OpenStack</a></li>
  <li><a href="#appendix">Appendix - FAQ</a></li>
</ul>

{% endcapture %}


{% capture maincontent %}

  {% include /installguides/introduction.md %}
  {% include /installguides/get_start.md %}
  {% include /installguides/step1.md %}
  {% include /installguides/step2.md %}
  {% include /installguides/step3.md %}
  {% include /installguides/step4.md %}
  {% include /installguides/step5.md %}
  {% include /installguides/step6.md %}
  {% include /installguides/step7.md %}
  {% include /installguides/step8.md %}
  {% include /installguides/step9.md %}
  {% include /installguides/step10.md %}
  {% include /installguides/step11.md %}
  {% include /installguides/step12.md %}
  {% include /installguides/appendix.md %}

{% endcapture %}

{% include /userguides/template.html %}

