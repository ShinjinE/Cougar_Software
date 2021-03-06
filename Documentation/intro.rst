Introduction
============

This document is meant to be a technical guide for accessing, 
modifying, and expanding Cosmotron's software. This is not meant 
to be API documentation, but rather a guide for modifying the 
software on Cosmotron to adjust how the motors move, change the 
controller scheme, and possibly adjust the code to match 
modifications made to the physical movement mechanisms.

The following is a brief summarry of each section.

**Technical Manual**

    **Accessing the Raspberry Pi**

        How to access the files on the Raspberry Pi so they can be changed.

    **Changing Movement Range**

        How to change the ranges the motors on Cosmotron move.

    **Changing Movement Map**

        How to change the mapping of inputs to outputs.

**Input Event Handling**

    Brief documentation of the code that reads input events from the PS4 controllers.

**Movement Mapping**

    Brief documentation of the code that maps the PS4 inputs to the Maestro outputs.

**Output Objects**

    Brief documentation for each of the output objects used to calculate the Maestro outputs.