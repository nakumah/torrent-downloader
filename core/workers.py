import pandas as pd
from PySide6.QtGui import QIcon
import qtawesome as qta

from resources.app_colors import appColors


def extractIconName(ext: str, df: pd.DataFrame) -> str | None:
    """
    Extracts the icon name from the target dataframe. (font awesome 5 icon names)

    Arguments:
        ext (str): the file extension .e.g '.mp4'
        df (pd.DataFrame): the target dataframe, see `./resources/corpus/extensions.csv`

    Returns:
        tuple[str | None]: the icon name if found, None otherwise
    """
    match = df.loc[df['Extension'].str.lower() == ext, 'FA5Icon']
    if not match.empty:
        return match.values[0]
    return None

def getIconFromExtension(ext: str, df: pd.DataFrame, default="box") -> QIcon:
    """
    Resolves an icon from the target dataframe based on the file extension.
    Default value is `box`. (font awesome 5 icon names)

    Arguments:
        ext (str): the file extension .e.g '.mp4'
        df (pd.DataFrame): the target dataframe, see `./resources/corpus/extensions.csv`
        default (str): the default icon name - a box

    Returns:
        QIcon: the icon
    """
    icon_name = extractIconName(ext, df)
    if icon_name is None:
        icon = qta.icon(f"fa5s.{default}", color=appColors.medium_rgb)
    else:
        icon = qta.icon(f"fa5s.{icon_name}", color=appColors.medium_rgb)

    return QIcon(icon)


def getIconFromCategory(category: str, default="box") -> QIcon:
    """
    Resolves and icon from the target dataframe based on the category.
    Default is `box`

    Arguments:
        category (str): the category of the icon, see `https://github.com/hemantapkh/1337x/blob/main/py1337x/types/category.py`
        default (str): the default icon name - a box

    Returns:
        QIcon: the icon

    """
    # font awesome 5 icon names
    iconNames = {
        'movies': "film",
        'tv': "tv",
        'games': "gamepad",
        'music': "music",
        'apps': "cogs",
        'anime': "paw",
        'documentaries': "video",
        'xxx': "leaf",
        'other': "box",
    }

    icon = qta.icon(f"fa5s.{iconNames.get(category, default)}", color=appColors.medium_rgb)
    return QIcon(icon)