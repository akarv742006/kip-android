namespace Kingmakers.Localization
{
    public enum Language
    {
        English,
        Tamil
    }

    public static class LanguageExtensions
    {
        public static string ToCode(this Language lang)
        {
            return lang switch
            {
                Language.Tamil => "ta",
                _ => "en"
            };
        }

        public static Language FromCode(string code)
        {
            return code?.ToLower() switch
            {
                "ta" => Language.Tamil,
                _ => Language.English
            };
        }
    }
}
