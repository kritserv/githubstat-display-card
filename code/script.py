from bs4 import BeautifulSoup, NavigableString
import svgwrite
import requests
from datetime import date

text_dict_size = {
	4 : ['i', 'l'],
	5 : ['j', 't', 'I', '\\', '/', '!', '[', ']', ' ', '.', ':'],
	6 : ['f', '-', '(', ')', '"', '}', '{'],
	7 : ['r', '*'],
	8 : ['^'],
	9 : ['c', 'k', 's', 'v', 'x', 'y', 'z', 'J'],
	10 : ['a', 'b', 'd', 'e', 'g', 'h', 'n', 'o', 'p', 'q', 'u', 'L', '#', '?', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
	11 : ['F', 'T', 'Z', '+', '=', '>', '<'],
	12 : ['B', 'E', 'K', 'P', 'S', 'V', 'X', 'Y', '&', '_', '&'],
	13 : ['w', 'C', 'D', 'H', 'N', 'R', 'U'],
	14 : ['A', 'G', 'O', 'Q', '★'],
	15 : ['m', 'M'],
	16 : ['%'],
	17 : ['W'],
	18 : ['@', '$']
}

def TxtWidth(txt):
    total_length = 0
    used_dict = text_dict_size
    for char in txt:
        for length in used_dict:
            if char in used_dict[length]:
                total_length += length
    return total_length


def AddTxt(txt, pos, col_weight, dwg):
    color, weight = col_weight
    dwg.add(
        dwg.text(txt, insert=pos, fill=color, font_weight=weight, font_family="Arial")
    )


def AddRect(pos, size, color, dwg):
    dwg.add(dwg.rect(insert=pos, size=size, fill=color))


def AddCss(dwg):
    html_string = dwg.tostring()
    soup = BeautifulSoup(html_string, "html.parser")
    svg_tag = soup.find("svg")

    style_tag = soup.new_tag("style")

    CSS = """.blink {animation: blink 1s steps(2, start) infinite;} @keyframes blink { to { visibility: hidden;}}"""

    style_tag.append(NavigableString(CSS))

    svg_tag.append(style_tag)
    svg = str(svg_tag)

    return svg


def DrawSvg(context, bg_col, main_col, second_col, col, size_x, size_y):
    dwg = svgwrite.Drawing(profile="tiny")
    need_animate_css = False

    x_pos = 400

    AddRect((20, 0), (size_x, size_y), bg_col, dwg)

    AddTxt(context["username"], (x_pos, 20), (main_col, "bold"), dwg)
    AddTxt(
        "@",
        (
            x_pos
            + TxtWidth(
                context["username"],
            ),
            20,
        ),
        (second_col, "normal"),
        dwg,
    )
    AddTxt(
        context["pc_name"],
        (
            x_pos
            + TxtWidth(
                context["username"] + "@",
            ),
            20,
        ),
        (main_col, "bold"),
        dwg,
    )

    line = ""
    while (
        TxtWidth(
            line,
        )
        < TxtWidth(
            f"{context['username']}@{context['pc_name']}",
        )
        + 20
    ):
        line += "_ "

    AddTxt(line, (x_pos, 50), (second_col, "normal"), dwg)

    AddTxt("last year contrib: ", (x_pos, 80), (main_col, "bold"), dwg)
    AddTxt(
        context["contrib"],
        (
            x_pos
            + TxtWidth(
                "last year contrib: ",
            ),
            80,
        ),
        (second_col, "normal"),
        dwg,
    )

    AddTxt("info of top10 repos: ", (x_pos, 110), (main_col, "bold"), dwg)
    AddTxt(
        "by stargaze",
        (
            x_pos
            + TxtWidth(
                "info of top10 repos: ",
            ),
            110,
        ),
        (second_col, "normal"),
        dwg,
    )

    AddTxt("Total Stars: ", (x_pos, 140), (main_col, "bold"), dwg)
    AddTxt(
        str(context["all_stars"]) + " ★",
        (
            x_pos
            + TxtWidth(
                "Total Stars: ",
            ),
            140,
        ),
        (second_col, "normal"),
        dwg,
    )

    context["all_lang"] = (
        context["all_lang"]
        .replace("'", "")
        .replace("{", "")
        .replace("}", "")
        .split(",")
    )
    y_pos = 170

    count = 0
    for lang_and_amount in list(reversed(context["all_lang"])):
        # break if github user have more than 5 languages
        count += 1
        if count > 5:
            break
        lang, amount = lang_and_amount.split(":")

        AddTxt(f"{lang}: ", (x_pos, y_pos), (main_col, "bold"), dwg)
        AddTxt(
            amount,
            (
                x_pos
                + TxtWidth(
                    f"{lang}: ",
                ),
                y_pos,
            ),
            (second_col, "normal"),
            dwg,
        )
        y_pos += 30

    AddTxt("date: ", (x_pos, y_pos), (main_col, "bold"), dwg)
    AddTxt(
        context["latest_update"],
        (
            x_pos
            + TxtWidth(
                "date: ",
            ),
            y_pos,
        ),
        (second_col, "normal"),
        dwg,
    )
    y_pos += 30

    color_in_row = 0
    for color in col:
        if color_in_row > 7:
            color_in_row = 0
            y_pos += 30
            x_pos -= 30 * 8
        AddRect((x_pos, y_pos), (30, 20), col[color], dwg)
        color_in_row += 1
        x_pos += 30

    y_pos += 50
    AddTxt(context["username"], (20, y_pos), (main_col, "bold"), dwg)
    AddTxt(
        "@",
        (
            20
            + TxtWidth(
                context["username"],
            ),
            y_pos,
        ),
        (second_col, "normal"),
        dwg,
    )
    AddTxt(
        context["pc_name"] + ":",
        (
            20
            + TxtWidth(
                context["username"] + "@",
            ),
            y_pos,
        ),
        (main_col, "bold"),
        dwg,
    )
    AddTxt(
        "~$",
        (
            20
            + TxtWidth(
                f"{context['username']}@{context['pc_name']}:",
            ),
            y_pos,
        ),
        (second_col, "bold"),
        dwg,
    )

    blinktxt = dwg.text(
        "|",
        insert=(
            20
            + TxtWidth(
                f"{context['username']}@{context['pc_name']}:~$  ",
            ),
            y_pos,
        ),
        fill=main_col,
        font_weight="bold",
        font_family="Arial",
        class_="blink",
    )
    dwg.add(blinktxt)

    dwg = AddCss(dwg)

    return dwg


def ScrapDataFromGithub(username):
    url = "https://github.com"
    response = requests.get(f"{url}/{username}")

    if response.status_code != 200:
        return {"username": username, "message": response.status_code}, 201

    else:
        soup = BeautifulSoup(response.content, "html.parser")

        profile_img = soup.find("img", class_="avatar-user")["src"]
        last_year_contrib = (
            soup.find("div", class_="js-yearly-contributions")
            .find("h2")
            .text.split("\n")[1]
            .strip()
        )

        repo_url_response = requests.get(
            f"{url}/{username}/?tab=repositories&sort=stargazers"
        )

        if repo_url_response.status_code != 200:
            return {"username": username, "message": repo_url_response.status_code}, 201

        else:
            repo_soup = BeautifulSoup(repo_url_response.content, "html.parser")
            repo_elem_list = repo_soup.find(id="user-repositories-list").find_all("li")

            used_language_count_dict = {}
            total_stars = 0
            total_amounts = 0

            i = 0
            for repo_elem in repo_elem_list:
                # Top 10 repo by stargazer
                if i >= 10:
                    break

                else:
                    repo = repo_elem.find("a")["href"]
                    repo_url_response = requests.get(f"{url}/{repo}")
                    if repo_url_response.status_code != 200:
                        return {
                            "username": username,
                            "message": response.status_code,
                        }, 201

                    else:
                        repo_soup = BeautifulSoup(
                            repo_url_response.content, "html.parser"
                        )
                        repo_star = repo_soup.find(id="repo-stars-counter-star").text
                        if "k" in repo_star:
                            repo_star = repo_star[0:-1]
                            repo_star = float(repo_star) * 1000
                        else:
                            repo_star = float(repo_star)
                        total_stars += repo_star
                        for used_language_elem in repo_soup.find_all(
                            "a", class_="d-inline-flex"
                        ):
                            language, amount = used_language_elem.find_all("span")
                            try:
                                used_language_count_dict[language.text] += float(
                                    amount.text[0:-1]
                                )
                                total_amounts += float(amount.text[0:-1])
                            except:
                                used_language_count_dict[language.text] = float(
                                    amount.text[0:-1]
                                )
                                total_amounts += float(amount.text[0:-1])

                i += 1

            if total_stars > 999:
                total_stars = str(round(total_stars / 1000, 2)) + "k"
            else:
                total_stars = str(int(total_stars))
            sorted_language = sorted(
                used_language_count_dict.items(), key=lambda item: item[1]
            )
            used_language_count_dict = dict(sorted_language)
            for language in used_language_count_dict:
                used_language_count_dict[language] = str(
                    round(used_language_count_dict[language] / total_amounts * 100, 2)
                )

            return (
                username,
                profile_img,
                last_year_contrib,
                total_stars,
                str(used_language_count_dict),
                str(date.today()),
            )


data = ScrapDataFromGithub("kritserv")

col = {
    "black": "#171421",
    "red": "#C01C28",
    "green": "#26A269",
    "brown": "#A2734C",
    "darkblue": "#12488B",
    "darkpurple": "#A347BA",
    "cyan": "#2AA1B3",
    "lightgrey": "#D0CFCC",
    "grey": "#5E5C64",
    "lightred": "#F66151",
    "lightgreen": "#33D17A",
    "yellow": "#E9AD0C",
    "blue": "#2A7BDE",
    "purple": "#C061CB",
    "skyblue": "#33C7DE",
    "white": "#FFFFFF",
}

result_context = {
    "username": data[0],
    "contrib": data[2],
    "all_stars": data[3],
    "all_lang": data[4],
    "latest_update": data[5],
    "pc_name": "test",
}

result = DrawSvg(result_context, col["black"], col["cyan"], col["white"], col, 700, 450)
# add terminal transparency
result = result.replace("></rect>", ' fill-opacity="0.95"></rect>')
# add background image
result = result.replace(
    "</defs>",
    "</defs><svg xmlns='http://www.w3.org/2000/svg'><rect fill='#000000' width='2000' height='1500'/><defs><rect  stroke='#000000' stroke-width='0.8' width='1' height='1' id='s'/><pattern id='a' width='3' height='3' patternUnits='userSpaceOnUse' patternTransform='scale(39.4) translate(-974.62 -730.96)'><use  fill='#242424' href='#s' y='2'/><use  fill='#242424' href='#s' x='1' y='2'/><use  fill='#333333' href='#s' x='2' y='2'/><use  fill='#333333' href='#s'/><use  fill='#3e3e3e' href='#s' x='2'/><use  fill='#3e3e3e' href='#s' x='1' y='1'/></pattern><pattern id='b' width='7' height='11' patternUnits='userSpaceOnUse' patternTransform='scale(39.4) translate(-974.62 -730.96)'><g  fill='#484848'><use href='#s'/><use href='#s' y='5' /><use href='#s' x='1' y='10'/><use href='#s' x='2' y='1'/><use href='#s' x='2' y='4'/><use href='#s' x='3' y='8'/><use href='#s' x='4' y='3'/><use href='#s' x='4' y='7'/><use href='#s' x='5' y='2'/><use href='#s' x='5' y='6'/><use href='#s' x='6' y='9'/></g></pattern><pattern id='h' width='5' height='13' patternUnits='userSpaceOnUse' patternTransform='scale(39.4) translate(-974.62 -730.96)'><g  fill='#484848'><use href='#s' y='5'/><use href='#s' y='8'/><use href='#s' x='1' y='1'/><use href='#s' x='1' y='9'/><use href='#s' x='1' y='12'/><use href='#s' x='2'/><use href='#s' x='2' y='4'/><use href='#s' x='3' y='2'/><use href='#s' x='3' y='6'/><use href='#s' x='3' y='11'/><use href='#s' x='4' y='3'/><use href='#s' x='4' y='7'/><use href='#s' x='4' y='10'/></g></pattern><pattern id='c' width='17' height='13' patternUnits='userSpaceOnUse' patternTransform='scale(39.4) translate(-974.62 -730.96)'><g  fill='#515151'><use href='#s' y='11'/><use href='#s' x='2' y='9'/><use href='#s' x='5' y='12'/><use href='#s' x='9' y='4'/><use href='#s' x='12' y='1'/><use href='#s' x='16' y='6'/></g></pattern><pattern id='d' width='19' height='17' patternUnits='userSpaceOnUse' patternTransform='scale(39.4) translate(-974.62 -730.96)'><g  fill='#000000'><use href='#s' y='9'/><use href='#s' x='16' y='5'/><use href='#s' x='14' y='2'/><use href='#s' x='11' y='11'/><use href='#s' x='6' y='14'/></g><g  fill='#585858'><use href='#s' x='3' y='13'/><use href='#s' x='9' y='7'/><use href='#s' x='13' y='10'/><use href='#s' x='15' y='4'/><use href='#s' x='18' y='1'/></g></pattern><pattern id='e' width='47' height='53' patternUnits='userSpaceOnUse' patternTransform='scale(39.4) translate(-974.62 -730.96)'><g  fill='#35FFF7'><use href='#s' x='2' y='5'/><use href='#s' x='16' y='38'/><use href='#s' x='46' y='42'/><use href='#s' x='29' y='20'/></g></pattern><pattern id='f' width='59' height='71' patternUnits='userSpaceOnUse' patternTransform='scale(39.4) translate(-974.62 -730.96)'><g  fill='#35FFF7'><use href='#s' x='33' y='13'/><use href='#s' x='27' y='54'/><use href='#s' x='55' y='55'/></g></pattern><pattern id='g' width='139' height='97' patternUnits='userSpaceOnUse' patternTransform='scale(39.4) translate(-974.62 -730.96)'><g  fill='#35FFF7'><use href='#s' x='11' y='8'/><use href='#s' x='51' y='13'/><use href='#s' x='17' y='73'/><use href='#s' x='99' y='57'/></g></pattern></defs><rect fill='url(#a)' width='100%' height='100%'/><rect fill='url(#b)' width='100%' height='100%'/><rect fill='url(#h)' width='100%' height='100%'/><rect fill='url(#c)' width='100%' height='100%'/><rect fill='url(#d)' width='100%' height='100%'/><rect fill='url(#e)' width='100%' height='100%'/><rect fill='url(#f)' width='100%' height='100%'/><rect fill='url(#g)' width='100%' height='100%'/></svg>",
)
# add foreground image
result = result.replace(
    "</rect><text",
    "</rect><svg xmlns='http://www.w3.org/2000/svg' width='330' height='330' x='40' y='20' ><rect fill='#18FFC8' width='1600' height='800'/><g fill-opacity='1'><polygon  fill='#2fe4f5' points='800 100 0 200 0 800 1600 800 1600 200'/><polygon  fill='#44a7ec' points='800 200 0 400 0 800 1600 800 1600 400'/><polygon  fill='#587de4' points='800 300 0 600 0 800 1600 800 1600 600'/><polygon  fill='#736cde' points='1600 800 800 400 0 800'/><polygon  fill='#a17dd8' points='1280 800 800 500 320 800'/><polygon  fill='#c08ed4' points='533.3 800 1066.7 800 800 600'/><polygon  fill='#D19ECF' points='684.1 800 914.3 800 800 700'/></g></svg><text",
)
with open("githubstat_card.svg", "w") as f:
    f.write(result)
