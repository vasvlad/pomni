# Mnemosyne configuration file.

# Upload server. Only change when prompted by the developers.
upload_server = "xxxxmnemosyne-proj.dyndns.org:80"
upload_logs = False

# Set to True to prevent you from accidentally revealing the answer
# when clicking the edit button.
only_editable_when_answer_shown = False

# The number of daily backups to keep. Set to -1 for no limit.
backups_to_keep = 5

# The moment the new day starts. Defaults to 3 am. Could be useful to
# change if you are a night bird. You can only set the hours, not
# minutes, and midnight corresponds to 0.
day_starts_at = 3

# Latex preamble.
latex_preamble = """
\documentclass[12pt]{article}
\pagestyle{empty}
\begin{document}
"""

# Latex postamble.
latex_postamble = "\end{document}"

# Latex command.
latex = "latex"

# Latex dvipng command.
dvipng = "dvipng -D 200 -T tight tmp.dvi"

# path to default theme
theme_path = "./hildon-UI/rainbow"
