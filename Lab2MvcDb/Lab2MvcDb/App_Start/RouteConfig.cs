using System.Web.Mvc;
using System.Web.Routing;

namespace Lab2MvcDb
{
    public class RouteConfig
    {
        public static void RegisterRoutes(RouteCollection routes)
        {
            routes.IgnoreRoute("{resource}.axd/{*pathInfo}");

            routes.MapRoute(
                name: "Default",
                url: "{controller}/{action}/{index}",
                defaults: new { controller = "Database", action = "Index", index = UrlParameter.Optional }
            );
        }
    }
}
