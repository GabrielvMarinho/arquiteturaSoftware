package com.example.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class Teste {

    @GetMapping("/getDados")
    public String getDados(){
        return "Serviço funcionando...";
    }
}
