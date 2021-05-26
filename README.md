# FEH Weapon Skill Simulator
[Try it out here](https://fehskillsim.herokuapp.com/)

Because of new prf weapons that come out that look like encyclopedias, it would be fun to guess what the new prfs will be.
Using existing skill "phrases" such as "if unit initiates combat" and "unit makes a guaranteed follow-up attack", the app generates a brand new prf.

Uses Flask for python web integration, Pillow for image editing.

# Functionality
Add a weapon name and supply parameters such as "weapon type" (e.g. melee or tome), "move type" (e.g. armor or flying),
and "power" from weak to broken.
Output as a text string and as an image that looks like the images on FEH banner trailers.
