---
layout: page
title: mailinglist
---
{% include JB/setup %}


{% capture subhead %}
  <h1>How To Contribute</h1>
  <p class="lead"></p>
{% endcapture %}

{% capture maincontent %}
<a name='top'></a>
<h2>Contents</h2>
<ul>
    <li>
        <a href='#How_can_i_help'>
            <span>1</span>
            <span>How can I help?</span>
        </a>
    </li>
        <ul>
            <li>
                <a href='#If_you_are_a_developer'>
                    <span>1.1</span>
                    <span>If you are a developer</span>
                </a>
            </li>
                <ul>
                    <li>
                        <a href='#Bug_fixing'>
                            <span>1.1.1</span>
                            <span>Bug fixing</span>
                        </a>
                    </li>
                    <li>
                        <a href='#Housekeeping'>
                            <span>1.1.2</span>
                            <span>Housekeeping</span>
                        </a>
                    </li>
                    <li>
                        <a href='#Feature_development'>
                            <span>1.1.3</span>
                            <span>Feature development</span>
                        </a>
                    </li>
                    <li>
                        <a href='#Reviewing'>
                            <span>1.1.4</span>
                            <span>Reviewing</span>
                        </a>
                    </li>
                </ul>
            <li>
                <a href='#If_you_are_a_tester'>
                    <span>1.2</span>
                    <span>If you are a tester</span>
                </a>
            </li>
        </ul>
    <li>
        <a href='#Developer_guide_of_compass_manual'>
            <span>2</span>
            <span>Developer's Guide of Compass Manual</span>
        </a>
    </li>
        <ul>
            <li>
                <a href='#Quick_reference'>
                    <span>2.1</span>
                    <span>Quick reference</span>
                </a>
            </li>
            <li>
                <a href='#Getting_started'>
                    <span>2.2</span>
                    <span>Getting started</span>
                </a>
            </li>
                <ul>
                    <li>
                        <a href='#Account_setup'>
                            <span>2.2.1</span>
                            <span>Account setup</span>
                        </a>
                    </li>
                    <li>
                        <a href='#Setting_up_git_configuration'>
                            <span>2.2.2</span>
                            <span>Setting up git configuration</span>
                        </a>
                    </li>
                    <li>
                        <a href='#Installing_git_review'>
                            <span>2.2.3</span>
                            <span>Installing git-review</span>
                        </a>
                    </li>
                    <li>
                        <a href='#Starting_work_on_project'>
                            <span>2.2.4</span>
                            <span>Starting work on project</span>
                        </a>
                    </li>
                </ul>
            <li>
                <a href='#Development_workflow'>
                    <span>2.3</span>
                    <span>Development workflow</span>
                </a>
            </li>
                <ul>
                    <li>
                        <a href='#Working_on_bugs'>
                            <span>2.3.1</span>
                            <span>Working on bugs</span>
                        </a>
                    </li>
                    <li>
                        <a href='#Working_on_specifications_blueprints'>
                            <span>2.3.2</span>
                            <span>Working on specifications and blueprints</span>
                        </a>
                    </li>
                    <li>
                        <a href='#Compass_core_structure'>
                            <span>2.3.4</span>
                            <span>Compass-core structure</span>
                        </a>
                    </li>
                    <li>
                        <a href='#Testing_compass_project'>
                            <span>2.3.5</span>
                            <span>Testing Compass project</span>
                        </a>
                    </li>
                    <li>
                        <a href='#Starting_a_change'>
                            <span>2.3.6</span>
                            <span>Starting a change</span>
                        </a>
                    </li>
                    <li>
                        <a href='#Committing_a_change'>
                            <span>2.3.7</span>
                            <span>Committing a change</span>
                        </a>
                    </li>
                    <li>
                        <a href='#Submitting_a_change_for_review'>
                            <span>2.3.8</span>
                            <span>Submitting a change for review</span>
                        </a>
                    </li>
                    <li>
                        <a href='#Updating_a_change'>
                            <span>2.3.9</span>
                            <span>Updating a change</span>
                        </a>
                    </li>
                </ul>
            <li>
                <a href='#Code_review'>
                    <span>2.4</span>
                    <span>Code review</span>
                </a>
                    </li>
        </ul>
</ul>


<h2 id='How_can_i_help'>How can I help?</h2>

<p>Please join our communication forums:

<ul>
    <li>Subscribe <a href="https://groups.google.com/a/syscompass.org/forum/?hl=en#!forum/users">Compass users Google Group</a>.</li>
    <li>Send email to <a href="mailto:dev@syscompass.org">dev@syscompass.org</a>.</li>
</ul>
</p>

<h2 id='If_you_are_a_developer'>If you're an developer</h2>
<ul>
    <li>Check out how we work</li>
        <ul>
             <li>What is <a href='https://wiki.openstack.org/wiki/Compass'>compass</a>, and how it works.</li>
        </ul>
    <li>Read the <a href='#'>Developer's Guide of Compass Manual</a> to get started</li>
    <li>Learn how to work with Openstack Gerrit review system.</li>
    <li>Review code</li>
</ul>


<h3 id='Bug_fixing'>Bug fixing</h3>
<p>You can start to contribute with bug fixing. Confirmed bugs are usually good targets. Here is the list of <a href='https://bugs.launchpad.net/compass'>bugs</a> that have been reported.</p>
<p>You can provide instruction on how to fix a certain bug. Or you can directly fix it: assign the bug to youself, set the status to <i>IN PROGRESS</i>,
branch the code, implement the fix, and propose your change. Once your fix has been merged, come back and add a commit then check the status to <i>FIX COMMITTED</i>.</p>


<h3 id='Housekeeping'>Housekeeping</h3>
<p>Maitaining good code quality is a non-stopping work that share with all development team member. There are always several constant work you can help with. For instance, adding explaining comments in code, reducing pylint violations, increasing code coverage. Those are good ways to get involved, and it will let you to get familiar with different part of code.</p>


<h3 id='Feature_development'>Feature development</h3>
<p>Once you are comfortable with the code, you can start to share your idea by contributing new feature. We use Openstack Launchpad Blueprints and Specs to track the design and implementation of significant features. By using blueprint, you can propose a deign and contain the sepcification.</p>
<p>To get start, you need to follow this process:</p>
<ul>
    <li>Register your bluepring in Launchpad by going to <a href='https://blueprints.launchpad.net/compass'>https://blueprints.launchpad.net/compass</a> and clicking "Register a blueprint"</li>
    <li>Git clone https://github.com/stackforge/compass-specs.git</li>
    <li>You can find an example spec in specs/template.rst</li>
    <li>Get it reviewed by submitting your patch using Gerrit</li>
    <li>Assignee sets implementation status to "Implemented" when the work is completed</li>
</ul>
<p>For more information, please see: <a href='https://wiki.openstack.org/wiki/Blueprints'>https://wiki.openstack.org/wiki/Blueprints</a></p>


<h3 id='Reviewing'>Reviewing</h3>
<p>Every patch submitted needs to get reviewed before it can be approved or merged. Any developer in compass team can be your reviewer.
Before you add reviewer, you change needs to pass automated testing. When a new patch is submitted, Jenkins and Compass CI will run the project's tests on the patch. Once completed, Jenkins and Compass CI will report test result to gerrit in the form of a Verified: +/-1 vote. You will need one developer and one menager's reviews to be approved and merged.</p>
<p>For more information, please see: <a href='http://docs.openstack.org/infra/manual/developers.html#code-review'>http://docs.openstack.org/infra/manual/developers.html#code-review</a>


<h2 id='If_you_are_a_tester'>If you are a tester</h2>
<p>We need you to make sure that Compass behaves correctly. Feel free to try compass and report any <a href='https://bugs.launchpad.net/compass'>issue</a>. For how to install compass, please see <a href='http://www.syscompass.org/install.html'>Try Compass</a> for more information.</p>


<h1 id='Developer_guide_of_compass_manual'>Developer guide of compass manual</h1>
<h2 id='Quick_reference'>Quick reference</h2>
<img src='img/how_to_contribute.png' style='width: 700px;'>

<h2 id='Getting_started'>Getting started</h2>
<p>The purpose of this part is to walk you through the concepts and specificactions that should be understood before contributing the Compass.</p>

<p>Before you get into details of the project, a few steps need to be compeleted. Such as setting up a few account on required webstie, signing a contributor license agreement, uploading an ssh key, and installing git-review.</p>

<h3 id='Account_setup'>Account setup</h3>
<p>First of all, you will need a <a href='https://launchpad.net/+login'>Launchpad account</a>, since this is how the Gerrit Code Review system will identify you.
Then, do not forget to <a href='https://www.openstack.org/join/'>join The OpenStack Foundation</a> which is free and required for all code contributors.
Please make sure you use same email address as the one for code contributions, since this will need to match your preferred email address in Gerrit.</p>
<p>Visit <a href='https://review.openstack.org/'>https://review.openstack.org/</a> and click the "Sign In" link at the top-right corner of the page. Login with your Launchpad ID.
The first time you login OpenStack's Gerrit, you will nee to select a unique username.</p>

<p>Every contributor needs to agree to the <a href='https://review.openstack.org/#/settings/agreements'>Individual Contributor License Agreement</a> and provide <a href='https://review.openstack.org/#/settings/contact'>contact information</a>.


<h3 id='Setting_up_git_configuration'>Setting up git configuration</h3>
<p>Run these steps to set up the git configuration. Please ensure the email matches the one in your Gerrit contact information:</p>
<pre>git config --global user.name "Firstname Lastname"
git config --global user.email "your_email@youremail.com"</pre>
<p>To check your git configuration:</p>
<pre>git config --list</pre>

<p>You will also want to upload an SSH key to Gerrit at <a href='https://review.openstack.org/#/settings/ssh-keys'>review.openstack.org</a>, so that you will be able to commit changes for review later.</p>


<h3 id='Installing_git_review'>Installing git-review</h3>
<p>Git-review is a git subcommand that handles all the details of working with Gerrit. Before you start work, make sure git-review has been installed.</p>

<p>On Ubuntu(12.04) or later, git-review is included in the distribution, so install it as any other package:</p>
<pre>apt-get install git-review</pre>

<p>On Fedora 16 and later, Red Hat Enterprise Linux, and CentOS 6.5 and later, you must enable the <a href='http://fedoraproject.org/wiki/EPEL/FAQ#howtouse'>EPEL</a> repository first, then install the package:</p>
<pre>yum install git-review</pre>
<p>All of git-review's interactions with gerrit are sequences of normal git commands.
If you want to know more about what it is doing, just add -v to the options and it will print out all of the commands it is running.</p>


<h3 id='Starting_work_on_project'>Working on the project</h3>
<p>Clone Compass:</p>
<pre>git clone git://git.openstack.org/stackforge/compass-core.git</pre>
<p>You may want to ask git-review to configure your project to bind with Gerrit. If you do not do it at this point, it will do so the first time you submit a patch.
But you may want to do this ahead of time. To do so:</p>
<pre>cd compass-core
git review -s</pre>
<p>Git-review checks that you can log in to gerrit with your ssh key.
It assumes that your gerrit/launchpad user name is the same as the current name. If the user name does not match, it asks you to enter your gerrit/launchpad user name. You can avoid that question by typing the following:</p>
<pre>git config --global gitreview.username yourgerritusername</pre>
<p>If you do not remember your Gerrit user name go to the <a href='https://review.openstack.org/#/settings/'>settings page</a> on gerrit to check it out (it is not your email address).</p>


<h2 id='Development_workflow'>Development workflow</h2>

<h3 id='Working_on_bugs'>Working on bugs</h3>
<p>Bug reports for the project are tracked on Launchpad at <a href='https://bugs.launchpad.net/compass'>https://bugs.launchpad.net/compass</a>.
Contributor may review these reports regularly when looking for work to tackle.</p>

<p>When working on bugs, there are four aspects you need to notice:</p>
<ul>
    <li>When a bug is filed, it is set to "New" status. A "New" bug can be set to "Confirmed" once it has been reproduced and is confirmed as authentic.</li>
    <li>Make sure the bug has been marked "In Progress" if it is assigned.</li>
    <li>If information that caused bugs to be marked as "Incomplete" has been provided, see if more information is required and remind bug reporter if they have not responded after 2-4 weeks.</li>
    <li>Check with assignee if the bug is still being worked on. If not, unassign it and mark it back to "Confirmed".</li>
</ul>

<p>Once you find a bug that you are interested in, assign it to youself. When you submit a patch, please include the bug information  in the commit message as reference so Gerrit can create a link to the bug.
The following options are available:</p>
<pre>Closes-Bug: #1234567 -- use 'Closes-Bug' if the commit is intended to fully fix and close the bug being referenced.
Partial-Bug: #1234567 -- use 'Partial-Bug' if the commit is only a partial fix and more work is needed.
Related-Bug: #1234567 -- use 'Related-Bug' if the commit is merely related to the referenced bug.</pre>


<h3 id='Working_on_specifications_blueprints'>Working on specifications and blueprints</h3>
<p>Compass project has a specs repository which is used to hold approved design specifications for feature and changes to the project.</p>
<p>You can find an example spec in <code>specs/template.rst</code></p>
<p>Check the repository to learn about the organization.</p>
<pre>git clone https://github.com/stackforge/compass-specs.git</pre>
<p>Specifications are proposed by adding them to the <code>specs/"release"</code>directory and submit it for review.
Launchpad blueprints were used to track the implementation of these significant features and changes in Compass.
The implementation status of a blueprint can be found at the <a href='https://blueprints.launchpad.net/compass'>blueprint</a> in Launchpad.</p>


<h3 id='Compass_core_structure'>Compass-core structure</h3>
<p>After you checkout the Compass project, go inside <code>compass-core</code> directory and take a look at the structure. Here we are going to briefly explain <code>compass-core/compass</code>,
<code>compass-core/conf</code> and <code>compass-core/misc</code>.</p>
<ul>
    <li>Compass: All python code goes here.</li>
    <li>Conf: These config files are used by compass to deploy clusters, not for compass service itself.</li>
    <li>Misc: Contains miscellaneous config files used by system services such as ntp and apache. These services configs are modified specifically for compass service to use.</li>
</ul>


<h3 id='Testing_compass_project'>Testing Compass project</h3>
<p>Before starting to work on the code, it is necessary to test if Compass code runs properly in your local environment. It is recommended to use tox the tun the unit tests.</p>
<p>It is suggested you install tox with pip:</p>
<pre>[apt-get | yum] install python-pip
pip install tox</pre>

<p>If you are using python 2.6, run following under compass-core directory:</p>
<pre>tox -epy26</pre>
<p>For python 2.7, run:</p>
<pre>tox -epy27</pre>

<p>The test result may return with report syas: "EnvironmentError: mysql_config not found".
Sometimes mysql_config is missing on your system or the installer could not find it. Be sure mysql_config is really installed.</p>
<p>For CentOS 6.5 and later, run:</p>
<pre>yum python-devel mysql-devel</pre>
<p>For Ubuntu(12.04) or later, run:</p>
<pre>apt-get install libmysqlclient-dev python-dev</pre>


<h3 id='Starting_a_change'>Starting a change</h3>
<p>Once your local repository is set up, you can start contribute.</p>
<p>Make sure you have the latest upstream changes:</p>
<pre>git remote update
git pull origin</pre>
<p>Once you are done with the changing, you need to run style checks and unit tests to make sure the code is still executable.</p>
<pre>tox -epep8
tox -epy26</pre>


<h3 id='Committing_a_change'>Committing a change</h3>
<p>Git commit messages explain the chage in detail. If your changes are  related to a blueprint or a bug, be sure to mention them in the commit message using the following syntax:</p>
<pre>Implements: blueprint BLUEPRINT
Closes-Bug: ####### (Partial-Bug or Related-Bug are options)</pre>


<h3 id='Submitting_a_change_for_review'>Submitting a change for review</h3>
<p>Once you have committed a change to your local repository, all you need to do to send it to Gerrit for code review:</p>
<pre>git review</pre>


<h3 id='Updating_a_change'>Updating a change</h3>
<p>If you need to make additional changes, make and amend the changes to the existing commit. Leave the Change-ID the way it is. Gerrit knows this is an updated patch for an existing change.</p>
<pre>git commit --amend
git review</pre>


<h2 id='Code_review'>Code review</h2>
<p>When a new patch is uploaded to Gerrit, project's tests are run on the patch by Jenkins and Compass are run by Compass CI. Once completed the test result are reported to Gerrit in the form of a Verified: +/-1 vote.</p>
<p>If a change fails tests in Jenkins or Compass CI, please follow the steps below:</p>
<ul>
    <li>Jenkins and Compass CI leave comments with links to the log files for the test run. Follow those links and check out the output.It will include a console log.</li>
    <li>Examine the console log to determine the cause of the error. If it is related to your change, go fix the problem and upload a new patchset.</li>
    <li>It may be the case that the error is caused by non-deterministic reason like time out which is unrelated to your change. To re-run check, leave a comment on the review: "recheck compassci".
</ul>

<p>Compass requires more than two positive reviews from core team to approve. You need to choose one reviewer from developers and the other from core reviewers. Once the core reviewer you chose believe it is ready, he or she will mrege your change.</p>
<p>Here is the name list of Compass core team(listed alphabetically):</p>
<ul>
    <li>Core reviewer</li>
        <ul>
            <li>Weidong Shao</li>
            <li>Shuo Yang</li>
        </ul>
    <li>Developer</li>
        <ul>
            <li>Xicheng Chang</li>
            <li>Sam Su</li>
            <li>Xiaodong Wang</li>
            <li>Grace Yu</li>
            <li>Jerry Zhao</li>
        </ul>
</ul>




{% endcapture %}
{% include /getinvolved/template.html %}
<a href='#top'>Back to Top</a>
