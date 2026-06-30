CREATE TABLE IF NOT EXISTS `tarea2_appweb`.`nota` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `actividad_id` INT NOT NULL,
  `nota` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_nota_actividad1_idx` (`actividad_id` ASC),
  CONSTRAINT `fk_nota_actividad1`
    FOREIGN KEY (`actividad_id`)
    REFERENCES `tarea2_appweb`.`actividad` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
