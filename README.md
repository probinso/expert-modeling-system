# Expert Modeling System (EMS)

The expert modeling system provides tools to develop a Subject Matter Expert matching
system, from an attributed corpus, based on the Author-Topic-Model.
This was a prototype developed for NASA's Jet Propultion lab that matches tickets 
describing late stage mission critical anomalies with best candidate subject matter 
experts.

# User Story

For mission critical anomalies, described as engineering faults that effect late stage
and deployed missions, an engineering ticket is opened. In the body of this ticket there
is a free-text description of the anomaly occuring. The process of matching an expert, to
solve a ticket, could take several weeks and was usually handled by word of mouth and 
monopolizing on tribal knowlege. 

This program includes the pre-processing, processing, model building, and prototyped
information retrieval system that automates this expensive and faulty HR task. Given
as few as 30 words, from the ticket description (which are usually 600+) we are able to
match the correct engineer to close tickets within the first 15 suggestions. 

# Implementation and Installation Notes

The program is located in the `./code` directory, including notes on how to configure the
model for training and hosting to a local site.
