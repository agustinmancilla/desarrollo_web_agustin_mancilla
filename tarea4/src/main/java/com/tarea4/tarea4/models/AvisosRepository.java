package com.tarea4.tarea4.models;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;



@Repository
public interface AvisosRepository extends JpaRepository<Aviso_adopcion, Long> {
    Page<Aviso_adopcion> findAllByOrderByIdDesc(Pageable pageable);
}
