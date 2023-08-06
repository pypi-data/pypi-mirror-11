from __future__ import print_function
from gitlint import rules
from gitlint import display


class GitLinter(object):
    def __init__(self, config):
        self.config = config
        self.display = display.Display(config)

    @property
    def body_line_rules(self):
        return [rule for rule in self.config.body_rules if isinstance(rule, rules.LineRule)]

    @property
    def body_multiline_rules(self):
        return [rule for rule in self.config.body_rules if isinstance(rule, rules.MultiLineRule)]

    @property
    def title_line_rules(self):
        return [rule for rule in self.config.title_rules if isinstance(rule, rules.LineRule)]

    def _apply_line_rules(self, lines, rules, line_nr_start):
        """ Iterates over the lines in a given git commit message and applies all the enabled line rules to
        each line """
        all_violations = []
        line_nr = line_nr_start
        for line in lines:
            for rule in rules:
                violations = rule.validate(line)
                if violations:
                    for violation in violations:
                        violation.line_nr = line_nr
                        all_violations.append(violation)
            line_nr += 1
        return all_violations

    def _apply_multiline_rules(self, lines, rules):
        all_violations = []
        for rule in rules:
            violations = rule.validate(lines)
            if violations:
                all_violations.extend(violations)
        return all_violations

    def lint_commit_message(self, commit_message):
        # determine commit message title, commit message body, ignore lines starting with a #
        lines = [line for line in commit_message.split("\n") if not line.startswith("#")]
        commit_message_title = [lines[0]]
        commit_message_body = lines[1:] if len(lines) > 1 else []

        # determine violations by applying all rules
        violations = self._apply_line_rules(commit_message_title, self.title_line_rules, 1)
        violations.extend(self._apply_line_rules(commit_message_body, self.body_line_rules, 2))
        violations.extend(self._apply_multiline_rules(commit_message_body, self.body_multiline_rules))

        # sort violations by line number
        violations.sort(key=lambda v: v.line_nr)  # sort violations by line number
        return violations

    def print_violations(self, violations):
        """ Print a given set of violations to the standard error output """
        for v in violations:
            self.display.e("{}: {}".format(v.line_nr, v.rule_id), exact=True)
            self.display.ee("{}: {} {}".format(v.line_nr, v.rule_id, v.message), exact=True)
            self.display.eee("{}: {} {}: \"{}\"".format(v.line_nr, v.rule_id, v.message, v.content), exact=True)
