# Arch After Install

This repository contains my dotfiles with program to automatic install and apply my configuration.

## Pre requirements

- Arch linux _(if you use [archinstall](https://wiki.archlinux.org/title/Archinstall) use minimal profile)_
- Python, pip

## Installation

Follow this script:

```bash
git clone https://github.com/Konsyliarz42/arch-after-install.git
cd arch-after-install

python -m venv .venv
source ./.venv/bin/activate

pip install -r requirements.txt
```

## Usage

Run the code by command:

```bash
source ./.venv/bin/activate
python -m app
```

## Terminal preferences

> I do not include this as dotfiles for compatibility with multiple terminals.

**Font name:** [Source Code Pro](https://adobe-fonts.github.io/source-code-pro/) \
**Font size:** 12

|           | Text                                       | Background                                 |
| --------- | ------------------------------------------ | ------------------------------------------ |
| Default   | <span style="color:#ECEFF1">#ECEFF1</span> | <span style="color:#263238">#263238</span> |
| Bold      | <span style="color:#B0BEC5">#B0BEC5</span> | -                                          |
| Cursor    | <span style="color:#B0BEC5">#B0BEC5</span> | <span style="color:#455A64">#455A64</span> |
| Highlight | <span style="color:#B0BEC5">#B0BEC5</span> | <span style="color:#455A64">#455A64</span> |

|         |                                            |                                            |
| ------- | ------------------------------------------ | ------------------------------------------ |
| Black   | <span style="color:#9E9E9E">#9E9E9E</span> | <span style="color:#616161">#616161</span> |
| Red     | <span style="color:#E57373">#E57373</span> | <span style="color:#F44336">#F44336</span> |
| Green   | <span style="color:#AED581">#AED581</span> | <span style="color:#8BC34A">#8BC34A</span> |
| Yellow  | <span style="color:#FFD54F">#FFD54F</span> | <span style="color:#FFC107">#FFC107</span> |
| Blue    | <span style="color:#64B5F6">#64B5F6</span> | <span style="color:#2196F3">#2196F3</span> |
| Magneta | <span style="color:#BA68C8">#BA68C8</span> | <span style="color:#9C27B0">#9C27B0</span> |
| Cyan    | <span style="color:#4DD0E1">#4DD0E1</span> | <span style="color:#4DD0E1">#4DD0E1</span> |
| White   | <span style="color:#FAFAFA">#FAFAFA</span> | <span style="color:#EEEEEE">#EEEEEE</span> |
