<center>

<img src="updated_preview_img/githubstat.svg" width="700" height="450">

</center>

```
<img src="https://neoflask.pythonanywhere.com/?username=kritserv&img=flask&main_col=cyan&theme=solarized" width="700" height="450">
```

## ⚠️ Caution

When you put the above code on README file, it may not update your `githubstat` as expected. This is because the Neoflask web app is programmed to update user stats daily, but GitHub uses a cached (camo) version of the image instead of fetching the image from the original source.

## Recommended Approach

To ensure your `githubstat` is updated correctly, consider using a bot that automatically updates the image on a schedule. Then, use the path of the updated image as the source in the image tag displayed on your GitHub README.

```
<img src="updated_preview_img/githubstat.svg" width="700" height="450">
```

Link to the bot <a href="/.github/workflows/update_image.yml">.github/workflows/update_image.yml</a>

#### Settings > Actions > General > (Scroll down to bottom) > Workflow permissions > Read and write permissions > save

You also need to do this in the repo settings to allow bot to commit.

<br>

# Neoflask 

Neoflask is a Github stat card that can be added to a profile’s markdown file. It is inspired by neofetch and built with Flask.

<br>

# Clone

```
git clone https://github.com/kritserv/neoflask.git
```

> Python3.10 Recommend

```
cd neoflask/code && pip install -r requirements.txt
```

```
python run.py
```

<br>

<img src="showcase/example_for_readme.svg" width="700" height="450">

<br>

## Customizable value

**username** <u>use your github username</u>

**theme** <a href="https://github.com/kritserv/neoflask/tree/main/code/app/frontend/theme">available theme</a> (use gnome_dark as default theme)

**img** <a href="https://github.com/kritserv/neoflask/tree/main/code/app/frontend/display_image">available image</a> (use octocat as default image)

**main_col** <a href="#Color_palette">available color name </a> (use lightgreen as default main color)

**second_col** <a href="#Color_palette">available color name </a> (default secondary color depends on theme (dark or light))

**bg_col** <a href="#Color_palette">available color name </a> (default background color depends on theme (dark or light))

**font** <a href="#Fonts">available font name </a> (use arial as default)

<br>

## Contribution

There are no rules, just make sure to describe what you contribute clearly. As long as this project improves, I’ll accept it. Also, be nice.

<br>

## License

<a href="https://github.com/kritserv/neoflask/blob/main/LICENSE">GNU General Public License v3.0</a>

<br>

## Color_palette

> Colors hex code will depends on selected theme.

- black
- red
- green
- brown
- darkblue
- darkpurple
- cyan
- lightgrey
- grey
- lightred
- lightgreen
- yellow
- blue
- purple
- skyblue
- white

## Fonts

- arial
- monospace
