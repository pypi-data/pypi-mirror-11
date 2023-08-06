# pyblosxomdrafts

A [PyBlosxom](https://pyblosxom.github.io/) plugin that lets you save draft
blog entries.

Any entries with a "drafts" folder anywhere in their path are considered drafts.
For example:

    entries/drafts/my-draft-post.txt
    entries/category/sub-category/drafts/another-draft-post.txt

Drafts will be filtered out from all index pages, such as the front page of
your blog, category pages, and feeds. But if you visit a draft's permalink
page (e.g. `/drafts/my-draft-post`) directly in your browser, then you'll see
the draft post rendered.


## Installation

Install the pyblosxomdrafts package from pip:

    pip install pyblosxomdrafts

Then add it to the `load_plugins` setting in your `config.py`:

    py["load_plugins"] = ['pyblosxomdrafts']
