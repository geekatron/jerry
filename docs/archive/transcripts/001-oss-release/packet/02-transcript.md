# Full Transcript

> **Title:** Jerry Framework Open-Source Release
> **Speaker:** Adam Nowak
> **Segments:** 50

---

## Transcript

### Topic: Jerry Framework Introduction (seg-0001 to seg-0010)

<a id="seg-0001"></a>
**[seg-0001]** **Adam Nowak:** Hey Claude, we're going to be talking about the outstanding effort uh for the Jerry framework.

<a id="seg-0002"></a>
**[seg-0002]** **Adam Nowak:** And Jerry is a Claude Code plugin

<a id="seg-0003"></a>
**[seg-0003]** **Adam Nowak:** with a series of skills

<a id="seg-0004"></a>
**[seg-0004]** **Adam Nowak:** that is to help mitigate context rock

<a id="seg-0005"></a>
**[seg-0005]** **Adam Nowak:** as well as

<a id="seg-0006"></a>
**[seg-0006]** **Adam Nowak:** uh let's see

<a id="seg-0007"></a>
**[seg-0007]** **Adam Nowak:** as well as a general problem solving framework.

<a id="seg-0008"></a>
**[seg-0008]** **Adam Nowak:** It has a couple of different tracks. It has a general problem solving framework and a NASA systems engineering problem solving framework. It has an orchestrator to be able to coordinate the skills and the agents. It has a transcription service and we'll also have a work tracker service.

<a id="seg-0009"></a>
**[seg-0009]** **Adam Nowak:** We are getting ready to release this as an open source

<a id="seg-0010"></a>
**[seg-0010]** **Adam Nowak:** project with an MIT license.

---

### Topic: Claude MD and Skills Optimization (seg-0011 to seg-0012)

<a id="seg-0011"></a>
**[seg-0011]** **Adam Nowak:** And we need to focus on the following action items. So we need to optimize our quad file.

<a id="seg-0012"></a>
**[seg-0012]** **Adam Nowak:** We need to optimize our skills because we have just been developing them to test their behaviors, and we haven't necessarily applied all the best practices, such as leveraging, decomposition, and imports.

---

### Topic: Orchestration Planning (seg-0013 to seg-0018)

<a id="seg-0013"></a>
**[seg-0013]** **Adam Nowak:** You will need to create an orchestration plan. Well, actually, first you will need to

<a id="seg-0014"></a>
**[seg-0014]** **Adam Nowak:** Yeah, you'll need to create an orchestration plan for this. I would like you to use all the available agents,

<a id="seg-0015"></a>
**[seg-0015]** **Adam Nowak:** or the best available agents, in both the NASA SE and the problem solving skill through the orchestration skill.

<a id="seg-0016"></a>
**[seg-0016]** **Adam Nowak:** I would like to ensure that we have um

<a id="seg-0017"></a>
**[seg-0017]** **Adam Nowak:** adversarial.

<a id="seg-0018"></a>
**[seg-0018]** **Adam Nowak:** Critics in the feedback loop and the feedback loops funnel back upwards so the upstream agent can adjust any kind of feedback.

---

### Topic: Best Practices Research (seg-0019 to seg-0026)

<a id="seg-0019"></a>
**[seg-0019]** **Adam Nowak:** And what I'd like you to do is research what are Claude code,

<a id="seg-0020"></a>
**[seg-0020]** **Adam Nowak:** plugin,

<a id="seg-0021"></a>
**[seg-0021]** **Adam Nowak:** and skill best practices, as well as writing Claude code or Claude. md file best practices.

<a id="seg-0022"></a>
**[seg-0022]** **Adam Nowak:** I need you to do high quality research where you can parallelize and put the agents in the background in order to find out and create a

<a id="seg-0023"></a>
**[seg-0023]** **Adam Nowak:** Documents that both humans and you

<a id="seg-0024"></a>
**[seg-0024]** **Adam Nowak:** can use for building skills with best practices. Eventually we will want to synthesize that down

<a id="seg-0025"></a>
**[seg-0025]** **Adam Nowak:** to rules and patterns that we can put into the dot claude rules and patterns folders respectively.

<a id="seg-0026"></a>
**[seg-0026]** **Adam Nowak:** We will also want to make runbooks and playbooks using the runbook and playbook templates.

---

### Topic: GitHub Repository Strategy (seg-0027 to seg-0029)

<a id="seg-0027"></a>
**[seg-0027]** **Adam Nowak:** Then we have other action items. We need to make sure that we have

<a id="seg-0028"></a>
**[seg-0028]** **Adam Nowak:** Um, a new GitHub repository. We are going to rename the current Jerry repository to something different like Jerry Internal, JerryCore, or Saucer Boy.

<a id="seg-0029"></a>
**[seg-0029]** **Adam Nowak:** We're going to create a new Jerry repository to make it public facing.

---

### Topic: User Experience and Documentation (seg-0030 to seg-0036)

<a id="seg-0030"></a>
**[seg-0030]** **Adam Nowak:** We need to work on runbooks and playbooks for how to use Jerry.

<a id="seg-0031"></a>
**[seg-0031]** **Adam Nowak:** And we need critic feedback loops in that one where the critique is thinking about the ideal user experience.

<a id="seg-0032"></a>
**[seg-0032]** **Adam Nowak:** For different levels of Claude knowledge. So someone that doesn't know anything about Claude, someone that has a good level of knowledge about Claude,

<a id="seg-0033"></a>
**[seg-0033]** **Adam Nowak:** uh, someone who has no knowledge about Jerry, someone who has a you know a medium knowledge of Jerry. So think about it as like the explain it to me like I'm five,

<a id="seg-0034"></a>
**[seg-0034]** **Adam Nowak:** then engineer, and then architect perspectives. So we need our playbooks to be criticized uh and be able to help those different

<a id="seg-0035"></a>
**[seg-0035]** **Adam Nowak:** um

<a id="seg-0036"></a>
**[seg-0036]** **Adam Nowak:** mental models.

---

### Topic: Work Tracker Skill Completion (seg-0037 to seg-0043)

<a id="seg-0037"></a>
**[seg-0037]** **Adam Nowak:** What else?

<a id="seg-0038"></a>
**[seg-0038]** **Adam Nowak:** Oh, and we're going to want to finish the bug, uh sorry, the work tracker skill. So we have um a bunch of information still in the ClaudeMD file at the root of the repository

<a id="seg-0039"></a>
**[seg-0039]** **Adam Nowak:** that needs to get extracted into the work tracker skill,

<a id="seg-0040"></a>
**[seg-0040]** **Adam Nowak:** and it needs to get decomposed, and it should leverage imports for those decomposed components that should always be pulled into memory, and everything else should just be as file references

<a id="seg-0041"></a>
**[seg-0041]** **Adam Nowak:** and hyperlinks

<a id="seg-0042"></a>
**[seg-0042]** **Adam Nowak:** so that you can load it contextually when it's necessary, and you also need to write those.

<a id="seg-0043"></a>
**[seg-0043]** **Adam Nowak:** Simple rules that you will understand about when to load those into context.

---

### Topic: Project 008 Feature Creation (seg-0044 to seg-0050)

<a id="seg-0044"></a>
**[seg-0044]** **Adam Nowak:** So yeah,

<a id="seg-0045"></a>
**[seg-0045]** **Adam Nowak:** I will continue thinking about what are the other exercises, but these are the ones that we need to prioritize.

<a id="seg-0046"></a>
**[seg-0046]** **Adam Nowak:** We will need to let's see we will want to create a new feature in project 008,

<a id="seg-0047"></a>
**[seg-0047]** **Adam Nowak:** and that feature will be

<a id="seg-0048"></a>
**[seg-0048]** **Adam Nowak:** essentially about

<a id="seg-0049"></a>
**[seg-0049]** **Adam Nowak:** preparing Jerry for open.

<a id="seg-0050"></a>
**[seg-0050]** **Adam Nowak:** OSS release.

---

## Segment Index

| Segment | Speaker | Topic | Key Content |
|---------|---------|-------|-------------|
| seg-0001 | Adam Nowak | Introduction | Opening |
| seg-0002 | Adam Nowak | Introduction | Jerry is Claude Code plugin |
| seg-0003 | Adam Nowak | Introduction | With skills |
| seg-0004 | Adam Nowak | Introduction | Mitigate context rot |
| seg-0008 | Adam Nowak | Introduction | Components overview |
| seg-0010 | Adam Nowak | Introduction | MIT license |
| seg-0011 | Adam Nowak | Optimization | Action items intro |
| seg-0012 | Adam Nowak | Optimization | Skills optimization |
| seg-0014 | Adam Nowak | Orchestration | Orchestration plan |
| seg-0018 | Adam Nowak | Orchestration | Critics in feedback |
| seg-0021 | Adam Nowak | Research | Best practices |
| seg-0025 | Adam Nowak | Research | Rules and patterns |
| seg-0028 | Adam Nowak | Repository | Rename strategy |
| seg-0029 | Adam Nowak | Repository | Public repo |
| seg-0033 | Adam Nowak | Documentation | Three perspectives |
| seg-0038 | Adam Nowak | Work Tracker | Extract from ClaudeMD |
| seg-0040 | Adam Nowak | Work Tracker | Decomposition strategy |
| seg-0046 | Adam Nowak | Feature | PROJ-008 feature |
| seg-0050 | Adam Nowak | Feature | OSS release |
