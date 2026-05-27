using System;
using System.Collections.Generic;
using System.Linq;
using System.Web.Mvc;
using Lab2MvcDb.Models;

namespace Lab2MvcDb.Controllers
{
    public class DatabaseController : Controller
    {
        private const string CurrentIndexSessionKey = "CurrentDatabaseRecordIndex";

        // Часть II, п.1: несколько экземпляров модели хранятся в List.
        // Номер текущего экземпляра сохраняется отдельно в Session.
        private static readonly List<DatabaseRecord> Records = new List<DatabaseRecord>
        {
            new DatabaseRecord
            {
                Id = 1,
                DatabaseName = "UniversityDB",
                DbmsName = "MS SQL Server",
                TableCount = 18,
                CreatedAt = new DateTime(2024, 9, 1),
                AdminEmail = "admin.university@example.com",
                IsNormalized = true,
                Description = "Учебная база данных для учета студентов, групп и дисциплин."
            },
            new DatabaseRecord
            {
                Id = 2,
                DatabaseName = "LibraryCatalog",
                DbmsName = "PostgreSQL",
                TableCount = 12,
                CreatedAt = new DateTime(2025, 2, 12),
                AdminEmail = "library.dba@example.com",
                IsNormalized = true,
                Description = "Каталог книг, читателей и выдачи литературы."
            },
            new DatabaseRecord
            {
                Id = 3,
                DatabaseName = "ShopStorage",
                DbmsName = "MySQL",
                TableCount = 9,
                CreatedAt = new DateTime(2025, 10, 3),
                AdminEmail = "shop.storage@example.com",
                IsNormalized = false,
                Description = "База данных склада интернет-магазина."
            }
        };

        public ActionResult Index()
        {
            return RedirectToAction("Details");
        }

        public ActionResult Details(int? index)
        {
            int currentIndex = NormalizeIndex(index ?? GetCurrentIndex());
            SaveCurrentIndex(currentIndex);
            ViewBag.CurrentIndex = currentIndex;
            ViewBag.TotalCount = Records.Count;
            return View(Records[currentIndex]);
        }

        public ActionResult Previous()
        {
            int currentIndex = NormalizeIndex(GetCurrentIndex() - 1);
            SaveCurrentIndex(currentIndex);
            return RedirectToAction("Details", new { index = currentIndex });
        }

        public ActionResult Next()
        {
            int currentIndex = NormalizeIndex(GetCurrentIndex() + 1);
            SaveCurrentIndex(currentIndex);
            return RedirectToAction("Details", new { index = currentIndex });
        }

        public ActionResult All()
        {
            ViewBag.CurrentIndex = GetCurrentIndex();
            return View(Records);
        }

        public ActionResult AllWithHelpers(bool? external)
        {
            TempData["UseExternalHelper"] = external ?? true;
            return View(Records);
        }

        public ActionResult Create()
        {
            return View(new DatabaseRecord
            {
                Id = GetNextId(),
                CreatedAt = DateTime.Today,
                IsNormalized = true
            });
        }

        [HttpPost]
        public ActionResult Create(DatabaseRecord record)
        {
            if (!ModelState.IsValid)
            {
                return View(record);
            }

            record.Id = GetNextId();
            Records.Add(record);
            SaveCurrentIndex(Records.Count - 1);
            return RedirectToAction("Details", new { index = Records.Count - 1 });
        }

        public ActionResult Edit(int? index)
        {
            int currentIndex = NormalizeIndex(index ?? GetCurrentIndex());
            SaveCurrentIndex(currentIndex);
            ViewBag.CurrentIndex = currentIndex;
            return View(Records[currentIndex]);
        }

        [HttpPost]
        public ActionResult Edit(int index, DatabaseRecord record)
        {
            int currentIndex = NormalizeIndex(index);

            if (!ModelState.IsValid)
            {
                ViewBag.CurrentIndex = currentIndex;
                return View(record);
            }

            Records[currentIndex] = record;
            SaveCurrentIndex(currentIndex);
            return RedirectToAction("Details", new { index = currentIndex });
        }

        private int GetCurrentIndex()
        {
            object value = Session[CurrentIndexSessionKey];
            return value is int ? (int)value : 0;
        }

        private void SaveCurrentIndex(int index)
        {
            Session[CurrentIndexSessionKey] = NormalizeIndex(index);
        }

        private int NormalizeIndex(int index)
        {
            if (Records.Count == 0)
            {
                return 0;
            }

            if (index < 0)
            {
                return Records.Count - 1;
            }

            if (index >= Records.Count)
            {
                return 0;
            }

            return index;
        }

        private int GetNextId()
        {
            return Records.Count == 0 ? 1 : Records.Max(item => item.Id) + 1;
        }
    }
}
