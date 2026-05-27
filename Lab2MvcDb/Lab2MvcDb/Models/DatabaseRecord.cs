using System;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;

namespace Lab2MvcDb.Models
{
    [DisplayName("Запись предметной области 'Базы данных'")]
    public class DatabaseRecord
    {
        [DisplayName("Код записи")]
        public int Id { get; set; }

        [DisplayName("Название базы данных")]
        [Required(ErrorMessage = "Введите название базы данных")]
        public string DatabaseName { get; set; }

        [DisplayName("СУБД")]
        [Required(ErrorMessage = "Введите название СУБД")]
        public string DbmsName { get; set; }

        [DisplayName("Количество таблиц")]
        [Range(1, 1000, ErrorMessage = "Количество таблиц должно быть от 1 до 1000")]
        public int TableCount { get; set; }

        [DisplayName("Дата создания")]
        public DateTime CreatedAt { get; set; }

        [DisplayName("E-mail администратора")]
        [DataType(DataType.EmailAddress)]
        [EmailAddress(ErrorMessage = "Введите корректный e-mail")]
        public string AdminEmail { get; set; }

        [DisplayName("Нормализована")]
        public bool IsNormalized { get; set; }

        [DisplayName("Описание назначения")]
        public string Description { get; set; }
    }
}
