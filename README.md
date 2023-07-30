<p align="center">
    <a href="#readme">
        <img alt="Until Zero - タイマー | logo" src="https://raw.githubusercontent.com/u8slvn/until-zero/main/images/logo-readme.png">
    </a>
</p>
<p align="center">
    <a href="https://github.com/u8slvn/until-zero/releases"><img alt="GitHub tag (with filter)" src="https://img.shields.io/github/v/release/u8slvn/until-zero"></a>
    <a href="https://github.com/u8slvn/until-zero/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/u8slvn/until-zero/ci.yml?label=CI" alt="CI"></a>
    <a href="https://coveralls.io/github/u8slvn/until-zero?branch=main"><img src="https://coveralls.io/repos/github/u8slvn/until-zero/badge.svg?branch=main" alt="Coverage Status"></a>
    <a href="https://app.codacy.com/gh/u8slvn/until-zero/dashboard"><img src="https://img.shields.io/codacy/grade/4eef0ac6cf9c4c5c90141316b723d2da" alt="Code Quality"></a>
    <a href="https://github.com/u8slvn/until-zero"><img src="https://img.shields.io/github/license/u8slvn/until-zero" alt="Project license"></a>
</p>

Until Zero - タイマー is toy program allowing to sequence multiple timer. It can be used as a [pomodoro](https://en.wikipedia.org/wiki/Pomodoro_Technique) timer or you can setup your own custom timers list.

<p align="center">
    <a href="#readme">
        <img alt="Until Zero - タイマー | main window" src="https://raw.githubusercontent.com/u8slvn/until-zero/main/images/until-zero-main-window.jpg">
    </a>
</p>

<p align="center">
    <a href="#readme">
        <img alt="Until Zero - タイマー | timers window" src="https://raw.githubusercontent.com/u8slvn/until-zero/main/images/until-zero-timers-window.gif">
    </a>
</p>

## 🚀 Quick Start

The timers sequence configuration field must respect the following syntax **without spaces**:

```
minutes:secondes + minutes:secondes + minutes:secondes + ...
```

Note that `:secondes` is non-mandatory and only `minutes` is needed to set a timer.

### 📚 Examples

- 1 minute: `1`
- 1 minute: `0:60`
- 3 x 5 minutes: `5+5+5`
- 1 minute **+** 2 minutes and 10 seconds: `1+2:10`
- 1 hour **+** 5 minutes and 30 seconds: `60+5+0:30`
- 1 day (24 x 60 minutes): `1440`

### ⏱️ Pomodoro

You can also use the pomodoro buttons to sequence your timers.

- `TASK`: 25 minutes
- `SHORT BREAK`: 5 minutes
- `LONG BREAK`: 20 minutes

If you plan 4 sessions with 2 short breaks and 1 long break you should get as result: `25+5+25+20+25+5+25`

### 🏁 Run

Once you configured your timers you can start the sequence by clicking on `START`. The timers window should appear in top of your screen, if the position does not please you, you can move it around by holding the drag zone on the right. If you want to reset the timers window position just double-click on the drag zone icon `⋮`.

## 🛑 Limitations

Until Zero - タイマー has some feature limitations:

- `minutes` max config value is `9999`
- `seconds` max config value is `9999`
- A maximum of `40` timers can be added to the sequence.
