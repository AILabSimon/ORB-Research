# TRANSCRIPTS — what is stored here and why

Full raw ASR transcripts are NOT stored (DECISION_LOG D-004). What is stored is a per-video
**evidence extract**: every rule-bearing passage, verbatim, with the caption track's own timestamp.

Source of the text: YouTube's own auto-generated (ASR) English caption track, fetched from the
player's signed `api/timedtext?...&fmt=json3` request. Profanity appears as `[ __ ]` because
YouTube masks it. Numbers spoken aloud are occasionally mis-transcribed by the ASR; where a number
matters it is flagged.

To re-check any quotation: open the video at the stated timestamp.
