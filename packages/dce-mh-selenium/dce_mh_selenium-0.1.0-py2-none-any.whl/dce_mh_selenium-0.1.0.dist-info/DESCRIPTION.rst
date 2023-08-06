## mh-selenium

Selenium stuff for DCE Matterhorn

## Getting started

1. Create & activate a virtualenv: `virtualenv venv && source venv/bin/activate`
2. `pip install dce-mh-selenium`
3. `mh_driver --help` for commands and `mh_driver [cmd] --help` for command options

## Example process

The following sequence of commands shows an example of how to upload some media
to the Matterhorn inbox, create symlinks to populate the inbox selection menu
in the **Upload Recording** UI, execute a number of uploads

**Note**: The initial inbox upload/symlink commands will prompt for the ssh 
login password. Obvs in an automated testing scenario you will need have either 
a passphraseless ssh key or AWS instance profiles set up.

#### 1. Upload the initial media to the inbox

`mh_driver inbox put -H [admin ip] -f path/to/presenter.mp4`
`mh_driver inbox put -H [admin ip] -f path/to/presentation.mp4`

#### 2. Create symlinks

This will create 10 inbox symlinks to each of the previously uploaded files, 
i.e., 10 identical presenter/presentation copies. Each copy will be named using
the sequence integer: `presenter_1.mp4`, `presenter_2.mp4`, etc.

`mh_driver inbox symlink -H [admin ip] -f presenter.mp4 -c 10`
`mh_driver inbox symlink -H [admin ip] -f presentation.mp4 -c 10`

#### 3. Check inbox contents (optional)

`mh_driver inbox list -H [admin ip]`

#### 4. Run the selenium upload tasks

The `uname` and `passwd` values here correspond to the Matthorn admin interface 
login.

```
    for i in `seq 1 10`; do mh_driver upload -u [uname] -p [passwd] --inbox --presenter presenter_${i}.mp4 --presentation presentation_${i}.mp4 [admin base_url] ; done
```

This *should* result in 10 processing workflows. The flakiness of Selenium + MH 
makes this not guaranteed.

#### 5. (later) execute the trim tasks

In a happy world you'll have a set of 10 of workflows that process their 
respective copies of the uploaded media and then pause/hold at the `editor` 
operation waiting for a human to intervene. We don't need stinking humans; we 
have Selenium!

`mh_driver trim -u [uname] -p [passwd] [admin base_url]`


## Troubleshooting

### Known issues

#### UnexpectedAlertPresentException: Alert Text: Could not resume Workflow: error

Check that Matterhron nodes, particularly admin, are not in maintenance state.

## Resources

* python selenium docs: https://selenium-python.readthedocs.org/index.html



dce-mh-selenium change log
==========================

0.1.0 (2015-09-14)
------------------

Initial release!


