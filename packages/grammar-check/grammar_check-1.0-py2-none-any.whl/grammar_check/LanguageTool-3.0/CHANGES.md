# LanguageTool Change Log

## 3.0 (2015-06-29)

#### Breton
  * updated FSA spelling dictionary from An Drouizig Breton Spellchecker 0.13
  * updated POS dictionary from Apertium (svn r61079)

#### Catalan
  * added new rules
  * fixed false alarms
  * added words suggested by users

#### English
  * added a few new rules
  * ConfusionProbabilityRule (only enabled with the `--languagemodel` option)
    has been rewritten and `homophones.txt` has been renamed to `confusion_sets.txt`
    and now only has few items enabled by default, the rest is commented out
    to improve quality (less false alarms).
    Also see http://wiki.languagetool.org/finding-errors-using-big-data

#### German
  * fixed some false alarms
  * updated to jwordsplitter 4.1 for better compound splitting
  * the spell checker offers correct suggestions now for
    incorrect past tense forms like "gehte" -> "ging" (useful
    mostly for non-native speakers)
  * added word frequency information to improve spelling suggestions (but this
    won't help for compounds which are not in the dictionary)

#### Polish
  * added new rules
  * fixed dozens of false alarms

#### Portuguese
  * added/improved several rules (started adding morphologic rules)

#### Russian
  * improved rules
  * updated spellchecker
  
#### Slovak
  * dictionary update and several new rules
  
#### Ukrainian
  * big dictionary update (thousands of new words, new tagging for pronouns)
  * improved sentence and word tokenization
  * improved tokenization and tagging of lowercase abbreviations
  * new grammar and styling rules
  * new spelling rules, especially for lowercase abbreviations with dots
  * improved compound word tagging 
  * improved some rules coverage
  * many new barbarism replacement suggestions
  
#### Bug Fixes
  * `UppercaseSentenceStartRule` didn't properly reset its state so that
    different errors could be found when e.g. `JLanguageTool.check()` got
    called twice with the same text.
  * `Authenticator.setDefault()` is now only called if it's allowed by
    the Java security manager. In rare cases, this might affect using
    external XML rule files as documented at
    http://wiki.languagetool.org/tips-and-tricks#toc9 (Github issue #255)
  
#### GUI (stand-alone version)
  * fixed auto-detection of text language, which didn't work after editing text
  * a directory with ngram data for the confusion rule can now be specified
    in the configuration dialog (English only for now), see 
    http://wiki.languagetool.org/finding-errors-using-big-data

#### Embedded server
  * performance improvements for checking small texts
    for the use case that creates a new `JLanguageTool` object
    for every check, as done by the embedded server (or multithreaded
    LT users in general)

#### Command-line
  * Fixed an error with the `--api` option that printed invalid XML
    for large documents or when the input was STDIN (Github issue #251)
  * Print some information to STDERR instead of STDOUT so the `--api`
    option makes more sense

#### API
  * added `MultiThreadedJLanguageTool.shutdown()` to clean up the thread pool
  * several deprecated methods and classes have been removed, e.g.
    * `Language.REAL_LANGUAGES` is now `Languages.get()`
    * `Language.LANGUAGES` is now `Languages.getWithDemoLanguage()` - but you will probably
       want to use `Languages.get()`
  * Other static methods from class `Language` have also been moved to `Languages`
  * `Language.addExternalRuleFile()` and `Language.getExternalRuleFiles()`
    have been removed. To add rules, load them with `PatternRuleLoader`
    and call `JLanguageTool.addRule()`.
  * `getAllRules()`, `getAllActiveRules()`, and `getPatternRulesByIdAndSubId()` 
    in class `JLanguageTool` used to call `reset()` for all rules. This is
    not the case anymore. `reset()` is now called when one of the `check()`
    methods is called. This shouldn't make a difference for all common use-cases.
  * `Language.setName()` has been removed. If you need to set the name,
    overwrite the `getName()` method instead.
  * `Rule.getCorrectExamples()/getIncorrectExamples()`, `PatternToken.getOrGroup()/getAndGroup()`
    and `RuleMatch.getSuggestedReplacements()` now return an unmodifiable list
  * `AbstractSimpleReplaceRule.getFileName()` and `AbstractWordCoherencyRule.getFileName()`
    have been removed, the sub classes are now themselves responsible for loading their data
  * Sub classes of `AbstractCompoundRule` are now responsible for loading the
    compound data themselves using `CompoundRuleData`
  * `AbstractCompoundRule.setShort(String)` has been removed and added as
    a constructor parameter instead.

#### Internal
  * updated to language-detector 0.5


## 2.9.1 (2015-05-14)

#### LO/AOO Integration
  *  fix `osl::Thread::Create failed` error message, see https://bugs.documentfoundation.org/show_bug.cgi?id=90740

## Older versions

See [CHANGES.txt](https://github.com/languagetool-org/languagetool/blob/master/languagetool-standalone/CHANGES.txt) for changes before 2.9.1.
